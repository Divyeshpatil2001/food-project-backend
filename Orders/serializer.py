from rest_framework import serializers
from .models import Orders

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_id', 'user', 'total_amount', 'payment_status', 'created_at', 'items']
        read_only_fields = ['user']