from decimal import Decimal as D
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string


from oscar.apps.basket.abstract_models import (
	AbstractLine, AbstractBasket)

from eupagoapps.bids.models import ProductBid

# Changes and comments by Jonas

class Basket(AbstractBasket):
	

	def add_product(self, product, quantity=1, options=None):
		"""
		We override add_product from AbstractBasket in order to
		store customer's bid instead of product original price.
		"""
		if options is None:
			options = []
		if not self.id:
			self.save()

		# Ensure that all lines are the same currency
		price_currency = self.currency
		stock_info = self.strategy.fetch_for_product(product)
		if price_currency and stock_info.price.currency != price_currency:
			raise ValueError((
				"Basket lines must all have the same currency. Proposed "
				"line has currency %s, while basket has currency %s")
				% (stock_info.price.currency, price_currency))

		if stock_info.stockrecord is None:
			raise ValueError((
				"Basket lines must all have stock records. Strategy hasn't "
				"found any stock record for product %s") % product)

		# Line reference is used to distinguish between variations of the same
		# product (eg T-shirts with different personalisations)
		line_ref = self._create_line_reference(
			product, stock_info.stockrecord, options)


		line, created = self.lines.get_or_create(
			line_reference=line_ref,
			product=product,
			stockrecord=stock_info.stockrecord)

		if created:
			for option_dict in options:
				line.attributes.create(option=option_dict['option'],
									   value=option_dict['value'])

			bid_value = self.get_customer_bid(line.basket.owner, product)
			print(bid_value)

			line.quantity = quantity
			line.price_excl_tax = bid_value
			line.price_incl_tax = bid_value
			line.price_currency = stock_info.price.currency

			line.save()
			
		else:
			line.quantity = max(0, line.quantity + quantity)
			line.save()



		self.reset_offer_applications()

	def get_customer_bid(self, owner, product):
		""" Get the winner bid """
		# TODO finish status

		product_bid = ProductBid.objects.get(user=owner, product=product)#, status=ProductBid.APPROVED)

		if product_bid.user_bid3 is not None:
			return product_bid.user_bid3

		if product_bid.user_bid2 is not None:
			return product_bid.user_bid2

		if product_bid.user_bid1 is not None:
			return product_bid.user_bid1

		return None

	
	@property
	def current_total(self):
		if self.is_tax_known:
			return self.total_incl_tax
		return self.total_exc_tax

	@property
	def pagarme_credit(self):
		t = D(self.current_total)
		print('aehoo', t)
		c = t - D(0.029)*t - D(0.5)
		return c.quantize(D('0.01'))

	@property
	def pagarme_discount(self):
		total = D(self.current_total)
		credit = self.pagarme_credit
		discount = total - credit
		return discount.quantize(D('0.01'))

	@property
	def iugu_credit(self):
		t = D(self.current_total)
		c = t - D(0.0251)*t - D(0.7)
		return c.quantize(D('0.01'))

	@property
	def iugu_discount(self):
		total = D(self.current_total)
		credit = self.iugu_credit
		discount = total - credit
		return discount.quantize(D('0.01'))

	# https://pagseguro.uol.com.br/taxas-e-tarifas.jhtml#rmcl
	@property
	def pagseguro_credit(self):
		t = D(self.current_total)
		c = t - D(0.0399)*t - D(0.4)
		return c.quantize(D('0.01'))

	@property
	def pagseguro_discount(self):
		total = D(self.current_total)
		credit = self.pagseguro_credit
		discount = total - credit
		return discount.quantize(D('0.01'))


class Line(AbstractLine):
	"""
	Override properties to return the customer's bid instead
	of the original price
	"""

	@property
	def unit_price_excl_tax(self):
		return self.price_excl_tax

	@property
	def unit_price_incl_tax(self):
		return self.price_incl_tax

	def get_warning(self):
		"""
		We override it because even if a product's price changes, 
		it won't affect the customer because if only depends on their bid.
		"""
		return



from oscar.apps.basket.models import *  # noqa
