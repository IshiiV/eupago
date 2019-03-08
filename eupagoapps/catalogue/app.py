from oscar.apps.catalogue.app import CatalogueApplication as CoreCatalogueApplication

from django.conf.urls import url, include
from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.core.application import Application
from eupagoapps.bids.app import application as bids_app


class CatalogueApplication(CoreCatalogueApplication):
    app_name = 'catalogue'
    bids_app = bids_app

    def get_urls(self):
        urls = super(CatalogueApplication, self).get_urls()
        urls += [
            url(r'^(?P<product_slug>[\w-]*)_(?P<product_pk>\d+)/bids/',
                include(self.bids_app.urls)),
        ]
        return self.post_process_urls(urls)


application = CatalogueApplication()
