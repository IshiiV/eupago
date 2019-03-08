from django.db import models
from oscar.apps.payment import abstract_models
from django.utils.translation import ugettext_lazy as _
from eupagoapps.payment.managers import BankCardQuerySet

class Bankcard(abstract_models.AbstractBankcard):
	

	objects = BankCardQuerySet.as_manager()


from oscar.apps.payment.models import *