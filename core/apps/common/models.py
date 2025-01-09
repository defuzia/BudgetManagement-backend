from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedBaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Update date'),
        auto_now=True
    )

    class Meta:
        abstract = True
