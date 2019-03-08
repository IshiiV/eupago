from django.conf.urls import url, include
from django.contrib import admin
from oscar.app import application


from .views import BidDetailView

urlpatterns = [
	
	#url(r'^cbv/(?P<pk>\d+)', BidDetailView.as_view(), name='bid_detail'),
    # url(r'^(?P<id>\d+)', 'bids.views.bid_detail_view_func', name='bid_detail_function'),
    # url(r'^add/$', self.create_view.as_view(),name='reviews-add'),
]
