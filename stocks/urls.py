from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stocks.views.api import StockViewSet, PriceEntryViewSet

router = DefaultRouter()
router.register(r'stock', StockViewSet)
router.register(r'price-entry', PriceEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
