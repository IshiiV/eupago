from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CatalogueDashboardConfig(AppConfig):
    label = 'catalogue_dashboard'
    name = 'eupagoapps.dashboard.catalogue'
    verbose_name = _('Catalogue')
