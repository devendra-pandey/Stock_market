from rest_framework import serializers
from .models import Trade

class TradeSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()
    balance_quantity = serializers.ReadOnlyField()
    avg_purchase_price = serializers.ReadOnlyField()

    class Meta:
        model = Trade
        fields = '__all__'

    def create(self, validated_data):
        trade = Trade.objects.create(**validated_data)
        return trade
