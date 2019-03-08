
from oscar.apps.order.utils import OrderNumberGenerator as CoreOrderNumberGenerator


class OrderNumberGenerator(CoreOrderNumberGenerator):

    def order_number(self, basket=None):
        num = super(OrderNumberGenerator, self).order_number(basket)
        return "SHOP-%s" % num