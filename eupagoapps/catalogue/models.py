from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.utils.functional import cached_property

from oscar.apps.catalogue.abstract_models import AbstractProduct

class Product(AbstractProduct):
	
    def has_bid_by(self, user):
        if user.is_anonymous():
            return False
        return self.bids.filter(user=user).exists()

    def is_bid_permitted(self, user):
        """
        Determines whether a user may add a bid on this product.

        Default implementation respects OSCAR_ALLOW_ANON_BIDS and only
        allows leaving one bid per user and product.

        Override this if you want to alter the default behaviour; e.g. enforce
        that a user purchased the product to be allowed to leave a bid.
        """
        if user.is_authenticated() or settings.OSCAR_ALLOW_ANON_REVIEWS:
            return not self.has_bid_by(user)
        else:
            return False

    @cached_property
    def num_approved_bids(self):
        return self.bids.approved().count()

from oscar.apps.catalogue.models import *