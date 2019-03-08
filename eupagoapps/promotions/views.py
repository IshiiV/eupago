from django.views.generic import RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_class
from oscar.apps.promotions.views import HomeView as CoreHomeView

get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


class HomeView(CoreHomeView):
    context_object_name = "products"
   
    def get(self, request, *args, **kwargs):
        self.search_handler = self.get_search_handler(
        self.request.GET, request.get_full_path(), [])
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_search_handler(self, *args, **kwargs):
        return get_product_search_handler_class()(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx['summary'] = _("All products")
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name)
        ctx.update(search_context)
        return ctx