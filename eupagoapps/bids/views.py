from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, View

from eupagoapps.bids.signals import bid_added
from oscar.core.loading import get_classes, get_model
from oscar.core.utils import redirect_to_referrer
from decimal import Decimal

from eupagoapps.catalogue.models import Product
from eupagoapps.partner.models import StockRecord
from .models import ProductBid
from .forms import ProductBidForm
from babel.numbers import format_currency

Product = get_model('catalogue', 'product')

from django.http import HttpResponse, HttpResponseNotFound

class SimpleCreateProductBid(View):
    """ The bid dynamic is applied here """

    eupago_tax = Decimal('1.2')

    def user_bid_can_buy(self, vendor_bid, user_bid, remaining_bids):

        difference = Decimal(user_bid) - Decimal(vendor_bid) * self.eupago_tax
        print(difference, user_bid, vendor_bid, Decimal(vendor_bid) * self.eupago_tax)

        if difference > 0 : #É multiplicado 1.2, pra tirar 20% sobre o valor que o vendedor quer.
            bid_w_discount = Decimal(user_bid) - Decimal(difference/4)
            messages.success(self.request, _("Muito obrigado! Seu lance de %s foi aceito... conseguimos negociar com o nosso parceiro de vendas um descontinho e agora você vai adquirir o produto por %s" % (str(format_currency(user_bid, 'BRL', locale='pt_BR')), str(format_currency(bid_w_discount, 'BRL', locale='pt_BR')) ) ))
            return bid_w_discount

        elif difference == 0:
            messages.success(self.request, _("Muito obrigado! Seu lance de %s foi aceito e você pode comprar o produto." % str(format_currency(user_bid, 'BRL', locale='pt_BR'))))
            return user_bid

        else:
            if remaining_bids == 0:
                messages.warning(self.request, _("Seu lance de %s foi abaixo do esperado pelo vendedor. Seus lances acabaram, mas você pode comprar mais lances para essa oferta por apenas R$1,99 cada." % str(format_currency(user_bid, 'BRL', locale='pt_BR')) )) 
            else:
                messages.warning(self.request, _("Seu lance de %s foi abaixo do esperado pelo vendedor, tente outra vez! Você ainda tem %d chances." % (str(format_currency(user_bid, 'BRL', locale='pt_BR')), remaining_bids) )) 
            return user_bid

    def message_at_least_1_real_diff(self, source):
        messages.error(self.request, _("Seu lance precisa ter pelo menos R$1,00 de diferença em relação ao %s." % source))

    #stock = 70, 55, 40
    def post(self, request, *args, **kwargs):
        """ The new bid must have a difference of `min_difference` from old bid
            and must not be bigger than the product original price """
        import re

        bid = request.POST['bid']
        bid = re.sub('[R$ .]', '', bid) # R$ 100.000,00 => 100000,00
        bid = re.sub('[,]', '.', bid) # 100000.00

        min_difference = '1.00'

        product = get_object_or_404(Product, pk=kwargs['product_pk'])
        stock_record = get_object_or_404(StockRecord, product=product)
        

        try:
            product_bid = ProductBid.objects.get(user=request.user, product=product)
            
            # USER BID 3
            if product_bid.user_bid2 is not None and product_bid.user_bid3 is None:

                if Decimal(bid) - Decimal(product_bid.user_bid2) >= Decimal(min_difference):
                    product_bid.user_bid3 = self.user_bid_can_buy(stock_record.bid1, bid, 0)

                    product_bid.save()
                else:
                    self.message_at_least_1_real_diff('lance anterior')

            # USER BID 2
            elif product_bid.user_bid1 is not None and product_bid.user_bid2 is None:

                if Decimal(bid) - Decimal(product_bid.user_bid1) >= Decimal(min_difference):
                    product_bid.user_bid2 = self.user_bid_can_buy(stock_record.bid1, bid, 1)

                    product_bid.save()
                    
                else:
                    self.message_at_least_1_real_diff('lance anterior')

            # print(product_bid.pk)
            # print(product_bid.user_bid1, product_bid.user_bid2, product_bid.user_bid3)

        except ProductBid.DoesNotExist:

            # USER BID 1
            if Decimal(stock_record.price_excl_tax) - Decimal(bid) >= Decimal(min_difference):

                product_bid = ProductBid(user=request.user, product=product)
                product_bid.user_bid1 = self.user_bid_can_buy(stock_record.bid1, bid, 2)
                product_bid.save()

            else:
                self.message_at_least_1_real_diff('preço original')

        return redirect('catalogue:detail', product_slug=kwargs['product_slug'], pk=kwargs['product_pk'])


## NOT USED!
class CreateProductBid(CreateView):
    template_name = "catalogue/bids/bid_form.html"
    model = ProductBid
    product_model = ProductBid
    form_class = ProductBidForm
    view_signal = bid_added

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            self.product_model, pk=kwargs['product_pk'])
        # check permission to leave review
        if not self.product.is_bid_permitted(request.user):
            if self.product.has_bid_by(request.user):
                message = _("You have already made a bid on this product!")
            else:
                message = _("You can't leave without bid for this product.")
            messages.warning(self.request, message)
            return redirect(self.product.get_absolute_url())

        return super(CreateProductBid, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateProductBid, self).get_context_data(**kwargs)
        context['product'] = self.product
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateProductBid, self).get_form_kwargs()
        kwargs['product'] = self.product
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super(CreateProductBid, self).form_valid(form)
        self.send_signal(self.request, response, self.object)
        return response

    def get_success_url(self):
        messages.success(
            self.request, _("Thank you for make a bid for this product"))
        return self.product.get_absolute_url()

    def send_signal(self, request, response, bid):
        self.view_signal.send(sender=self, bid=rbid, user=request.user,
                              request=request, response=response)


class ProductBidDetail(DetailView):
    template_name = "catalogue/bids/bid_detail.html"
    context_object_name = 'bid'
    model = ProductBid

    def get_context_data(self, **kwargs):
        context = super(ProductBidDetail, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(
            Product, pk=self.kwargs['product_pk'])
        return context