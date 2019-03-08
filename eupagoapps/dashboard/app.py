from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.conf.urls import include, url

from oscar.core.application import DashboardApplication
from eupagoapps.bids.app import ProductBidApplication


class DashboardApplication(DashboardApplication):
    
    bids_app = ProductBidApplication()

    def get_urls(self):
        urls = [
            url(r'^bids/', include(self.bids_app.urls)),
        ]
        return self.post_process_urls(urls)


application = DashboardApplication()

from oscar.apps.dashboard.app import *
