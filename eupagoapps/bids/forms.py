from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ProductBid


class ProductBidForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)
    user_bid1 = forms.DecimalField(
        _("User bid 1"), decimal_places=2, max_digits=12)
    user_bid2 = forms.DecimalField(
        _("User bid 2"), decimal_places=2, max_digits=12)
    user_bid3 = forms.DecimalField(
        _("User bid 3"), decimal_places=2, max_digits=12)

    def __init__(self, product, user=None, *args, **kwargs):
        super(ProductBidForm, self).__init__(*args, **kwargs)
        self.instance.product = product
        if user and user.is_authenticated():
            self.instance.user = user
            del self.fields['name']
            del self.fields['email']

    class Meta:
        model = ProductBid
        fields = ('name', 'email', 'user_bid1', 'user_bid2', 'user_bid3')