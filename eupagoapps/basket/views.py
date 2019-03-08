from django import shortcuts
from oscar.apps.basket.views import BasketAddView as CoreBasketAddView

class BasketAddView(CoreBasketAddView):
	def post(self, request, *args, **kwargs):
		self.product = shortcuts.get_object_or_404(
			self.product_model, pk=kwargs['pk'])
		print(args)
		print(kwargs)
		print(self.product)

		return super(BasketAddView, self).post(request, *args, **kwargs)