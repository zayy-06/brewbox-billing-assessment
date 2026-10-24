from __future__ import annotations

import calendar
from datetime import date, timedelta
from decimal import Decimal
from typing import Callable

from .models import (
    CREDIT_VALID_DAYS,
    LATE_FEE,
    MAX_DISCOUNT_PERCENT,
    MAX_REFERRAL_CREDIT,
    REFERRAL_RATE,
    TAX_RATE,
    CreditEntry,
    Customer,
    Invoice,
    InvoiceStatus,
    LineKind,
    PausePeriod,
    Subscription,
    money,
)
from .repository import InMemoryRepository


class BillingService:
    """Application service for BrewBox subscription billing."""

    def __init__(
        self,
        repository: InMemoryRepository | None = None,
        today: Callable[[], date] | None = None,
    ) -> None:
        self.repo = repository or InMemoryRepository()
        self._today = today or date.today

    # ---------------------------------------------------------
    # Customers and subscriptions
    # ---------------------------------------------------------
    def create_customer(
        self,
        name: str,
        email: str,
        referral_code: str,
        referred_by: str | None = None,
    ) -> dict:
        email = email.strip().lower()
        referral_code = referral_code.strip().upper()

        if not name.strip():
            raise ValueError("customer name is required")
        if not email:
            raise ValueError("customer email is required")
        if not referral_code:
            raise ValueError("referral code is required")

        if any(c.email == email for c in self.repo.customers.values()):
            raise ValueError("email already registered")

        if self.repo.customer_by_referral_code(referral_code) is not None:
            raise ValueError("referral code already in use")

        if referred_by is not None:
            referred_by = referred_by.strip().upper()

            # FEAT-202: Validate referral code.
            if referred_by == referral_code:
                raise ValueError("self-referral is not allowed")

            referrer = self.repo.customer_by_referral_code(referred_by)
            if referrer is None:
                raise ValueError(f"unknown referral code: {referred_by!r}")

        customer = Customer(
            id=self.repo.next_id("cus"),
            name=name.strip(),
            email=email,
            referral_code=referral_code,
            referred_by=referred_by,
        )

        self.repo.customers[customer.id] = customer

        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "referral_code": customer.referral_code,
            "referred_by": customer.referred_by,
        }

    def create_subscription(
        self,
        customer_id: str,
        plan_code: str,
        addon_codes: tuple[str, ...] | list[str] = (),
        start_date: date | None = None,
        discount_percent: Decimal | int | str = Decimal("0"),
    ) -> dict:
        if customer_id not in self.repo.customers:
            raise ValueError("customer does not exist")

        if plan_code not in self.repo.plans:
            raise ValueError("unknown plan")

        unknown = [
            code for code in addon_codes
            if code not in self.repo.addons
        ]
        if unknown:
            raise ValueError(f"unknown add-on(s): {', '.join(unknown)}")

        discount = Decimal(str(discount_percent))

        # BUG-101: Validate discount.
        if discount < 0:
            raise ValueError("discount cannot be negative")

        if discount > MAX_DISCOUNT_PERCENT:
            raise ValueError(
                f"discount cannot exceed {MAX_DISCOUNT_PERCENT} percent"
            )

        subscription = Subscription(
            id=self.repo.next_id("sub"),
            customer_id=customer_id,
            plan_code=plan_code,
            addon_codes=tuple(addon_codes),
            start_date=start_date or self._today(),
            discount_percent=discount,
        )

        self.repo.subscriptions[subscription.id] = subscription

        return {
            "id": subscription.id,
            "customer_id": subscription.customer_id,
            "plan_code": subscription.plan_code,
            "addon_codes": subscription.addon_codes,
            "start_date": subscription.start_date,
            "discount_percent": subscription.discount_percent,
        }

    # ---------------------------------------------------------
    # Invoicing
    # ---------------------------------------------------------
    def issue_invoice(
        self,
        subscription_id: str,
        year: int,
        month: int,
        issued_on: date | None = None,
    ) -> Invoice | None:
        subscription = self.repo.subscriptions.get(subscription_id)

        if subscription is None:
            raise ValueError("subscription does not exist")

        if not 1 <= month <= 12:
            raise ValueError("month must be between 1 and 12")

        period_start, period_end = self._month_bounds(year, month)

        existing = self._find_invoice(subscription_id, year, month)
        if existing is not None:
            return existing

        if period_end < subscription.start_date:
            return None

        if (
            subscription.cancelled_on is not None
            and period_start >= subscription.cancelled_on
        ):
            return None

        active_days = self._active_days(
            subscription, period_start, period_end
        )

        if active_days == 0:
            return None

        issued = issued_on or self._today()
        plan = self.repo.plans[subscription.plan_code]
        days_in_month = calendar.monthrange(year, month)[1]

        # BUG-102 + FEAT-201:
        # Prorate using actual calendar days and exclude paused days.
        if active_days == days_in_month:
            factor = Decimal("1")
        else:
            factor = Decimal(active_days) / Decimal(days_in_month)

        plan_amount = money(plan.monthly_price * factor)

        addon_amounts = [
            (
                self.repo.addons[code],
                money(self.repo.addons[code].monthly_price * factor),
            )
            for code in subscription.addon_codes
        ]

        subtotal = money(
            plan_amount
            + sum(
                (amount for _, amount in addon_amounts),
                Decimal("0"),
            )
        )

        # BUG-101: Discount applies to plan only, not add-ons.
        discount_total = money(
            plan_amount
            * subscription.discount_percent
            / Decimal("100")
        )

        taxable = money(subtotal - discount_total)
        tax_total = money(taxable * TAX_RATE)

        invoice = Invoice(
            id=self.repo.next_id("inv"),
            customer_id=subscription.customer_id,
            subscription_id=subscription.id,
            period_start=period_start,
            period_end=period_end,
            issued_on=issued,
            due_on=issued + timedelta(days=14),
        )

        invoice.add_line(
            f"{plan.name} plan",
            plan_amount,
            LineKind.PLAN,
        )

        for addon, amount in addon_amounts:
            invoice.add_line(
                addon.name,
                amount,
                LineKind.ADDON,
            )

        if discount_total > 0:
            display_percent = format(
                subscription.discount_percent.normalize(), "f"
            )
            invoice.add_line(
                f"Discount {display_percent}%",
                -discount_total,
                LineKind.DISCOUNT,
            )

        invoice.add_line(
            "Sales tax (8.25%)",
            tax_total,
            LineKind.TAX,
        )

        invoice.subtotal = subtotal
        invoice.discount_total = discount_total
        invoice.tax_total = tax_total
        invoice.total = money(
            subtotal - discount_total + tax_total
        )

        # FEAT-202: Apply existing referral credits after tax.
        self._apply_available_credits(invoice, issued)

        self.repo.invoices[invoice.id] = invoice
        return invoice

    def issue_all_invoices(
        self,
        year: int,
        month: int,
    ) -> list[Invoice]:
        invoices: list[Invoice] = []

        for subscription_id in list(self.repo.subscriptions):
            invoice = self.issue_invoice(
                subscription_id, year, month
            )
            if invoice is not None:
                invoices.append(invoice)

        return invoices

    # ---------------------------------------------------------
    # Payments and late fees
    # ---------------------------------------------------------
    def record_payment(
        self,
        invoice_id: str,
        amount: Decimal | int | str | None = None,
        paid_on: date | None = None,
    ) -> Invoice:
        invoice = self._invoice(invoice_id)

        if invoice.status == InvoiceStatus.PAID:
            raise ValueError("invoice is already paid")

        if invoice.status == InvoiceStatus.VOID:
            raise ValueError("void invoice cannot be paid")

        due = invoice.amount_due
        paid = money(amount if amount is not None else due)

        if paid <= 0:
            raise ValueError("payment amount must be positive")

        if paid > due:
            raise ValueError("payment exceeds amount due")

        invoice.amount_paid = money(invoice.amount_paid + paid)
        payment_date = paid_on or self._today()

        if invoice.amount_due == 0:
            invoice.status = InvoiceStatus.PAID
            invoice.paid_on = payment_date

            # FEAT-202: Award referral credit when eligible.
            self._award_referral_credit(invoice, payment_date)

        return invoice

    def apply_late_fee(
        self,
        invoice_id: str,
        as_of: date | None = None,
    ) -> Invoice:
        invoice = self._invoice(invoice_id)
        day = as_of or self._today()

        if invoice.status != InvoiceStatus.ISSUED:
            return invoice

        if invoice.amount_due <= 0:
            return invoice

        # BUG-103: Five full grace days; fee starts on day six.
        if day <= invoice.due_on + timedelta(days=5):
            return invoice

        # Prevent applying the fee more than once.
        if invoice.late_fee > 0:
            return invoice

        invoice.add_line(
            "Late payment fee",
            LATE_FEE,
            LineKind.LATE_FEE,
        )

        invoice.late_fee = money(LATE_FEE)
        invoice.total = money(invoice.total + LATE_FEE)

        return invoice

    # ---------------------------------------------------------
    # Referral credits (FEAT-202)
    # ---------------------------------------------------------
    def credit_balance(
        self,
        customer_id: str,
        as_of: date | None = None,
    ) -> Decimal:
        day = as_of or self._today()
        total = Decimal("0.00")

        for entry in self.repo.credits.values():
            if (
                entry.customer_id == customer_id
                and entry.expires_on >= day
            ):
                total += entry.remaining

        return money(total)

    def list_credits(
        self,
        customer_id: str,
    ) -> list[CreditEntry]:
        entries = [
            entry
            for entry in self.repo.credits.values()
            if entry.customer_id == customer_id
        ]

        return sorted(entries, key=lambda entry: entry.expires_on)

    def _apply_available_credits(
        self,
        invoice: Invoice,
        as_of: date,
    ) -> None:
        eligible = sorted(
            (
                entry
                for entry in self.repo.credits.values()
                if entry.customer_id == invoice.customer_id
                and entry.expires_on >= as_of
                and entry.remaining > 0
            ),
            key=lambda entry: entry.expires_on,
        )

        remaining_due = invoice.amount_due

        for entry in eligible:
            if remaining_due <= 0:
                break

            applied = min(entry.remaining, remaining_due)

            entry.remaining = money(entry.remaining - applied)
            invoice.credit_applied = money(
                invoice.credit_applied + applied
            )
            remaining_due = money(remaining_due - applied)

    def _award_referral_credit(
        self,
        invoice: Invoice,
        paid_on: date,
    ) -> None:
        subscription = self.repo.subscriptions.get(
            invoice.subscription_id
        )

        if subscription is None:
            return

        customer = self.repo.customers.get(subscription.customer_id)

        if customer is None or customer.referred_by is None:
            return

        # Award only once per referred customer.
        already_awarded = any(
            entry.source_customer_id == customer.id
            for entry in self.repo.credits.values()
        )

        if already_awarded:
            return

        # The triggering invoice must be the first fully paid invoice.
        customer_invoices = self.repo.invoices_for_customer(customer.id)

        paid_invoices = sorted(
            (
                inv for inv in customer_invoices
                if inv.status == InvoiceStatus.PAID
            ),
            key=lambda inv: inv.paid_on or date.min,
        )

        if not paid_invoices or paid_invoices[0].id != invoice.id:
            return

        # Referral credit base excludes tax and existing credit applied.
        base = money(
            invoice.subtotal
            - invoice.discount_total
            - invoice.credit_applied
        )

        if base <= 0:
            return

        raw_credit = money(base * REFERRAL_RATE)
        credit_amount = min(raw_credit, MAX_REFERRAL_CREDIT)

        referrer = self.repo.customer_by_referral_code(
            customer.referred_by
        )

        if referrer is None:
            return

        entry = CreditEntry(
            id=self.repo.next_id("crd"),
            customer_id=referrer.id,
            source_customer_id=customer.id,
            source_invoice_id=invoice.id,
            amount=credit_amount,
            remaining=credit_amount,
            issued_on=paid_on,
            expires_on=paid_on + timedelta(days=CREDIT_VALID_DAYS),
            reason=f"Referral credit for customer {customer.id}",
        )

        self.repo.credits[entry.id] = entry

    # ---------------------------------------------------------
    # Pause / resume (FEAT-201)
    # ---------------------------------------------------------
    def pause_subscription(
        self,
        subscription_id: str,
        start: date,
        end: date,
        as_of: date | None = None,
    ) -> PausePeriod:
        subscription = self.repo.subscriptions.get(subscription_id)

        if subscription is None:
            raise ValueError("subscription does not exist")

        today = as_of or self._today()
        period = PausePeriod(start=start, end=end)

        if period.days < 7:
            raise ValueError(
                f"pause duration must be at least 7 days "
                f"(requested {period.days})"
            )

        if period.days > 90:
            raise ValueError(
                f"pause duration cannot exceed 90 days "
                f"(requested {period.days})"
            )

        if start < subscription.start_date:
            raise ValueError(
                "pause cannot start before the subscription start date"
            )

        if start < today:
            raise ValueError("pause start date cannot be in the past")

        for existing in subscription.pauses:
            if period.overlaps(existing):
                raise ValueError(
                    f"pause {start}–{end} overlaps existing pause "
                    f"{existing.start}–{existing.end}"
                )

        # Reject pausing when an invoice is overdue and unpaid.
        for invoice in self.repo.invoices_for_subscription(
            subscription_id
        ):
            if (
                invoice.status == InvoiceStatus.ISSUED
                and invoice.due_on < today
                and invoice.amount_due > 0
            ):
                raise ValueError(
                    "subscription has an overdue invoice; "
                    "settle it before pausing"
                )

        subscription.pauses.append(period)
        return period

    def resume_subscription(
        self,
        subscription_id: str,
        on: date,
    ) -> PausePeriod:
        subscription = self.repo.subscriptions.get(subscription_id)

        if subscription is None:
            raise ValueError("subscription does not exist")

        # Find a pause containing the requested resume date.
        active_pause: PausePeriod | None = None
        active_index = -1

        for index, pause in enumerate(subscription.pauses):
            if pause.start <= on <= pause.end:
                active_pause = pause
                active_index = index
                break

        if active_pause is None:
            raise ValueError(
                "no active pause covers the requested resume date"
            )

        # Resume date itself becomes an active day.
        new_end = on - timedelta(days=1)

        if new_end < active_pause.start:
            raise ValueError(
                "resume date cannot be on or before the pause start date"
            )

        shortened = PausePeriod(
            start=active_pause.start,
            end=new_end,
        )

        if shortened.days < 7:
            raise ValueError(
                f"early resume would leave only {shortened.days} "
                "paused day(s); minimum is 7"
            )

        subscription.pauses[active_index] = shortened
        return shortened

    def list_pauses(
        self,
        subscription_id: str,
    ) -> list[PausePeriod]:
        subscription = self.repo.subscriptions.get(subscription_id)

        if subscription is None:
            raise ValueError("subscription does not exist")

        return sorted(
            subscription.pauses,
            key=lambda pause: pause.start,
        )

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------
    def _invoice(self, invoice_id: str) -> Invoice:
        invoice = self.repo.invoices.get(invoice_id)

        if invoice is None:
            raise ValueError("invoice does not exist")

        return invoice

    @staticmethod
    def _month_bounds(
        year: int,
        month: int,
    ) -> tuple[date, date]:
        last_day = calendar.monthrange(year, month)[1]

        return (
            date(year, month, 1),
            date(year, month, last_day),
        )

    @staticmethod
    def _active_days(
        subscription: Subscription,
        period_start: date,
        period_end: date,
    ) -> int:
        """Count active billable days, excluding paused days."""
        start = max(period_start, subscription.start_date)
        end = period_end

        if start > end:
            return 0

        total = (end - start).days + 1

        for pause in subscription.pauses:
            overlap_start = max(start, pause.start)
            overlap_end = min(end, pause.end)

            if overlap_start <= overlap_end:
                total -= (overlap_end - overlap_start).days + 1

        return max(total, 0)

    def _find_invoice(
        self,
        subscription_id: str,
        year: int,
        month: int,
    ) -> Invoice | None:
        for invoice in self.repo.invoices.values():
            if (
                invoice.subscription_id == subscription_id
                and invoice.period_start.year == year
                and invoice.period_start.month == month
            ):
                return invoice

        return None