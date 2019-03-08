from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from oscar.core.application import Application
from oscar.core.loading import get_class
from eupagoapps.bids.views import (
    ProductBidDetail, CreateProductBid,
    SimpleCreateProductBid
    )

class ProductBidApplication(Application):
    name = None
    hidable_feature_name = "bids"

    detail_view = ProductBidDetail
    create_view = SimpleCreateProductBid

    def get_urls(self):
        urls = [
            url(r'^(?P<pk>\d+)/$', self.detail_view.as_view(),
                name='bids-detail'),
            url(r'^add/$', self.create_view.as_view(),
                name='bids-add'),
        ]
        return self.post_process_urls(urls)


application = ProductBidApplication()
