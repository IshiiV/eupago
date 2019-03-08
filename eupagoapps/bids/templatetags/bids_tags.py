# -*- coding: utf-8 -*- 
from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def is_bid_permitted(product, user):
    return product and product.is_bid_permitted(user)


from eupagoapps.catalogue.models import Product
from eupagoapps.partner.models import StockRecord
from eupagoapps.bids.models import ProductBid
from django.shortcuts import get_object_or_404, redirect
from babel.numbers import format_currency

@register.assignment_tag
def get_stock_and_bids(product_pk, user):
	product = get_object_or_404(Product, pk=product_pk)
	stock_record = get_object_or_404(StockRecord, product=product)

	
	html = ''
	total_bids = 0
	accept = False

	try:

		bids = ProductBid.objects.get(product=product, user=user)
		if bids.user_bid1:
			if bids.user_bid1 >= stock_record.bid1*Decimal('1.2'): #É multiplicado 1.2, pra tirar 10% sobre o valor que o vendedor quer.
				html += '<span style="color: blue">Lance 1 (%s) foi aceito</span><br>' % str(format_currency(bids.user_bid1, 'BRL', locale='pt_BR'))
				accept = True
			else:
				html += '<span style="color: red">Lance 1 (%s) não foi aceito</span><br>' % str(format_currency(bids.user_bid1, 'BRL', locale='pt_BR'))
			total_bids += 1

		if bids.user_bid2:
			if bids.user_bid2 >= stock_record.bid1*Decimal('1.2'): #É multiplicado 1.2, pra tirar 10% sobre o valor que o vendedor quer.
				html += '<span style="color: blue">Lance 2 (%s) foi aceito</span><br>' % str(format_currency(bids.user_bid2, 'BRL', locale='pt_BR'))
				accept = True
			else:
				html += '<span style="color: red">Lance 2 (%s) não foi aceito</span><br>' % str(format_currency(bids.user_bid2, 'BRL', locale='pt_BR'))
			total_bids += 1
		
		if bids.user_bid3:
			if bids.user_bid3 >= stock_record.bid1*Decimal('1.2'): #É multiplicado 1.2, pra tirar 10% sobre o valor que o vendedor quer.
				html += '<span style="color: blue">Lance 3 (%s) foi aceito</span><br>' % str(format_currency(bids.user_bid3, 'BRL', locale='pt_BR'))
				accept = True
			else:
				html += '<span style="color: red">Lance 3 (%s) não foi aceito</span><br>' % str(format_currency(bids.user_bid3, 'BRL', locale='pt_BR'))
			total_bids += 1

	except ProductBid.DoesNotExist:
		pass

	return { 'html': html, 'total_bids': total_bids, 'accept': accept }


@register.filter(name='add_eupago_tax')
def add_eupago_tax(value):
	return Decimal(value) * Decimal('1.2')
