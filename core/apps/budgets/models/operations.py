from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.budgets.models import Budget
from core.apps.common.models import TimestampedBaseModel
from core.apps.budgets.entities.operations import Category as CategoryEntity, Operation as OperationEntity
from core.apps.customers.models import Customer


class Category(TimestampedBaseModel):
    name = models.CharField(
        verbose_name=_('Category name'),
        max_length=255,
    )
    related_customer = models.ForeignKey(
        verbose_name=_('Related user id'),
        to=Customer,
        on_delete=models.CASCADE,
        related_name='categories',
    )

    def to_entity(self) -> CategoryEntity:
        return CategoryEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            related_customer=self.related_customer.to_entity(),
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Operation(TimestampedBaseModel):
    class OperationType(models.TextChoices):
        ADD = 'ADD', _('Addition')
        SUB = 'SUB', _('Subtraction')

    title = models.CharField(
        verbose_name=_('Operation name'),
        max_length=124,
        blank=True,
    )
    operation_type = models.CharField(
        verbose_name=_('Operation type'),
        max_length=3,
        choices=OperationType.choices,
        default=OperationType.ADD,
    )
    amount = models.DecimalField(
        verbose_name=_('Operation amount'),
        max_digits=11,
        decimal_places=2,
    )
    related_budget = models.ForeignKey(
        verbose_name=_('Related budget'),
        to=Budget,
        on_delete=models.CASCADE,
        related_name='operations',
    )
    related_category = models.ForeignKey(
        verbose_name=_('Related category'),
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='operations',
    )

    def to_entity(self) -> OperationEntity:
        return OperationEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            title=self.title,
            operation_type=self.operation_type,
            amount=self.amount,
            related_budget=self.related_budget.to_entity(),
            related_category=self.related_category.to_entity(),
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Operation')
        verbose_name_plural = _('Operations')
