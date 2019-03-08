from django import forms
from django.forms.models import inlineformset_factory

from oscar.apps.dashboard.catalogue.forms import (
    ProductForm as CoreProductForm,
    StockRecordForm as CoreStockRecordForm,
    StockRecordFormSet as CoreStockRecordFormSet,
)
# from oscar.apps.dashboard.catalogue.forms import StockRecordForm as CoreStockRecordForm
# from oscar.apps.dashboard.catalogue.forms import StockRecordFormSet as CoreStockRecordFormSet
from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'Product')
StockRecord = get_model('partner', 'StockRecord')

class ProductForm(CoreProductForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'is_discountable', 'structure']
        widgets = {
            'structure': forms.HiddenInput()
        }


class StockRecordForm(CoreStockRecordForm):
    
    class Meta:
        model = StockRecord
        fields = [
            'partner',
            # 'price_currency', 'price_excl_tax', 'price_retail', 'cost_price',
            'price_currency', 'price_excl_tax', 'bid1', 'bid2', 'bid3',
            'num_in_stock', 'low_stock_threshold',
        ]

# I had to copy the whole StockRecordFormSet because inheriting it was not working
# since StockRecord changes, so BaseStockRecordFormSet changes as well.

BaseStockRecordFormSet = inlineformset_factory(
    Product, StockRecord, form=StockRecordForm, extra=1)


class StockRecordFormSet(BaseStockRecordFormSet):

    def __init__(self, product_class, user, *args, **kwargs):
        self.user = user
        self.require_user_stockrecord = not user.is_staff
        self.product_class = product_class

        if not user.is_staff and \
           'instance' in kwargs and \
           'queryset' not in kwargs:
            kwargs.update({
                'queryset': StockRecord.objects.filter(product=kwargs['instance'],
                                                       partner__in=user.partners.all())
            })

        super(StockRecordFormSet, self).__init__(*args, **kwargs)
        self.set_initial_data()

    def set_initial_data(self):
        """
        If user has only one partner associated, set the first
        stock record's partner to it. Can't pre-select for staff users as
        they're allowed to save a product without a stock record.

        This is intentionally done after calling __init__ as passing initial
        data to __init__ creates a form for each list item. So depending on
        whether we can pre-select the partner or not, we'd end up with 1 or 2
        forms for an unbound form.
        """
        if self.require_user_stockrecord:
            try:
                user_partner = self.user.partners.get()
            except (exceptions.ObjectDoesNotExist,
                    exceptions.MultipleObjectsReturned):
                pass
            else:
                partner_field = self.forms[0].fields.get('partner', None)
                if partner_field and partner_field.initial is None:
                    partner_field.initial = user_partner

    def _construct_form(self, i, **kwargs):
        kwargs['product_class'] = self.product_class
        kwargs['user'] = self.user
        return super(StockRecordFormSet, self)._construct_form(
            i, **kwargs)

    def clean(self):
        """
        If the user isn't a staff user, this validation ensures that at least
        one stock record's partner is associated with a users partners.
        """
        if any(self.errors):
            return
        if self.require_user_stockrecord:
            stockrecord_partners = set([form.cleaned_data.get('partner', None)
                                        for form in self.forms])
            user_partners = set(self.user.partners.all())
            if not user_partners & stockrecord_partners:
                raise exceptions.ValidationError(
                    _("At least one stock record must be set to a partner that"
                      " you're associated with."))