from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string


from oscar.apps.order.abstract_models import AbstractLine

class Line(AbstractLine):
	"""
	Extend to include a redeem_code
	"""


	# format: [A-Z][A-Z][8 numbers] i.e. BG10000000, HY12345678
	# total: 26*26*10000000
	# for now we will use only 8 numbers
	redeem_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

	# True if customer has redeemed this line of product(s)
	redeemed = models.BooleanField(default=False)

	def generate_redeem_code(self):
		"""
		A redeem code must be unique and random, so we first check for its uniqueness
		"""

		already_exists = True
		code = None

		while already_exists:
			# code = get_random_string(length=2, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			code = ''
			code += get_random_string(length=8, allowed_chars='0123456789')
			print(code)

			try:
				obj = Line.objects.get(redeem_code=code)
			except Line.DoesNotExist:
				already_exists = False

		return code

	def save(self, *args, **kwargs):

		self.redeem_code = self.generate_redeem_code()
		return super(AbstractLine, self).save(*args, **kwargs)


from oscar.apps.order.models import *  # noqa
