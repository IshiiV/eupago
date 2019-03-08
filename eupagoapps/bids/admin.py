from django.contrib import admin

from .models import ProductBid


class ProductBidAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_bid1', 'user_bid2', 'user_bid3', 'status', 'date_created')


admin.site.register(ProductBid, ProductBidAdmin)





