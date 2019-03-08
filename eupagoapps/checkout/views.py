import logging

from django.views import generic
from oscar.core.loading import get_class, get_classes, get_model

from eupagoapps.payment.models import Bankcard
#BankcardForm = get_class('payment.forms', 'BankcardForm')

OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')


# PAYMENT 

def pagarme_value_from_total(total):
    t = Decimal(total)
    c = t - Decimal(0.029)*t - Decimal(0.5)
    return c.quantize(Decimal('0.01'))

def pagarme_discounts(total):
    total = Decimal(total)
    credit = pagarme_value_from_total(total)
    discount = total - credit
    return credit, discount.quantize(Decimal('0.01'))

def iugu_value_from_total(total):
    t = Decimal(total)
    c = t - Decimal(0.0251)*t - Decimal(0.7)
    return c.quantize(Decimal('0.01'))

def iugu_discounts(total):
    total = Decimal(total)
    credit = iugu_value_from_total(total)
    discount = total - credit
    return credit, discount.quantize(Decimal('0.01'))

# https://pagseguro.uol.com.br/taxas-e-tarifas.jhtml#rmcl
def pagseguro_value_from_total(total):
    t = Decimal(total)
    c = t - Decimal(0.0399)*t - Decimal(0.4)
    return c.quantize(Decimal('0.01'))

def pagseguro_discounts(total):
    total = Decimal(total)
    credit = pagseguro_value_from_total(total)
    discount = total - credit
    return credit, discount.quantize(Decimal('0.01'))


class PaymentDetailsView(OrderPlacementMixin, generic.TemplateView):
        
        #form_class = BankcardForm

        def post(self, request, *args, **kwargs):

                numero = request.POST['numero']
                nome = request.POST['nome']
                vencimento= request.POST['vencimento']
                
                bank_card = Bankcard.objects.get(user=request.user)


                bank_card.number = numero
                bank_card.name = nome
                bank_card.expiry_date = vencimento


        
              #  return redirect('catalogue:detail', product_slug=kwargs['product_slug'], pk=kwargs['product_pk'])


from oscar.apps.checkout.views import *