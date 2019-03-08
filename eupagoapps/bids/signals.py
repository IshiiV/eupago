import django.dispatch

bid_added = django.dispatch.Signal(
    providing_args=["bid", "user", "request", "response"])
