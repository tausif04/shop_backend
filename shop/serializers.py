from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class ShopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'id', 'owner', 'name', 'slug', 'city', 'state',
            'country', 'address', 'zip_code', 'phone', 'email',
            'description', 'logo_url', 'banner_url', 'status',
            'approval_date', 'commission_rate', 'created_at', 'updated_at'
        ]
