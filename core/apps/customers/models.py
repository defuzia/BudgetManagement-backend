from uuid import uuid4

from django.db import models

from core.apps.common.models import TimestampedBaseModel
from django.utils.translation import gettext_lazy as _

from core.apps.customers.entities.customers import Customer as CustomerEntity


class Customer(TimestampedBaseModel):
    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=20,
        unique=True,
    )
    token = models.CharField(
        verbose_name=_('Auth token'),
        max_length=255,
        unique=True,
        default=uuid4,
    )

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            phone=self.phone
        )

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

