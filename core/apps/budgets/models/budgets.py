from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.common.models import TimestampedBaseModel
from core.apps.budgets.entities.budgets import Currency as CurrencyEntity, Budget as BudgetEntity


class Currency(models.Model):
    name = models.CharField(
        verbose_name=_('Currency name'),
        max_length=124
    )
    short_name = models.CharField(
        verbose_name=_('Currency short name'),
        max_length=64,
        unique=True,
    )
    symbol = models.CharField(
        verbose_name=_('Currency symbol'),
        max_length=16,
    )

    def to_entity(self) -> CurrencyEntity:
        return CurrencyEntity(
            id=self.id,
            name=self.name,
            short_name=self.short_name,
            symbol=self.symbol
        )

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class Budget(TimestampedBaseModel):
    title = models.CharField(
        verbose_name=_('Budget name'),
        max_length=255
    )
    amount = models.DecimalField(
        verbose_name=_('Budget amount'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0'),
        blank=True
    )
    related_currency = models.ForeignKey(
        verbose_name=_('Related currency'),
        to=Currency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budgets'
    )
    related_user = models.UUIDField(
        verbose_name=_('Related user id')
    )

    def to_entity(self) -> BudgetEntity:
        return BudgetEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            title=self.title,
            amount=self.amount,
            related_currency=self.related_currency.to_entity(),
            related_user=self.related_user
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')
