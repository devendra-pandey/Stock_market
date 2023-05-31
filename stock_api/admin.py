from django.contrib import admin
from .models import Trade

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('date', 'company_name', 'trade_type', 'quantity', 'buy_price', 'amount', 'balance_quantity', 'avg_purchase_price')
