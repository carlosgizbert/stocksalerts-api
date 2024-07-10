from django.contrib import admin
from .models import Stock, PriceEntry

admin.site.register(Stock)
admin.site.register(PriceEntry)
