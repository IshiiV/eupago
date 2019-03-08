from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.partner.abstract_models import AbstractStockRecord

class StockRecord(AbstractStockRecord):
    # price_excl_tax is a product's original price

    bid1 =  models.DecimalField(
        _("Bid 1"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    bid2 =  models.DecimalField(
        _("Bid 2"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    bid3 =  models.DecimalField(
        _("Bid 3"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    class Meta:
        unique_together = False
    


from oscar.apps.partner.models import *