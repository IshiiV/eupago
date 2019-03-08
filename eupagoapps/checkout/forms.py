from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_model



Bankcard = get_model('payment', 'Bankcard')

class BancoForm(AuthenticationForm):


    number = forms.IntegerField(label=_("Card number"))
    ccv = forms.IntegerField(label=_("ccv"))
    expiry_month = forms.DateField(label=_("Expiry date"))
    start_month = forms.DateField(label=_("Expiry date"))


    class Meta:
        model = Bankcard
        fields = ('number', 'start_month', 'expiry_month', 'ccv')
   

# The BillingAddress form is in oscar.apps.payment.forms
from oscar.apps.checkout.forms import *