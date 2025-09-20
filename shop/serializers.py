# shop/serializers.py
from rest_framework import serializers
# Import the correct model names
from .models import Shops, ShopShopdocument, ShopShopattachment

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops # <-- Use the correct name
        fields = '__all__'

# ADDED THIS ENTIRE CLASS
class ShopDetailSerializer(serializers.ModelSerializer):
    """
    A more detailed serializer for a single shop view.
    """
    class Meta:
        model = Shops
        # Add any extra fields you want for the "detail" view
        fields = [
            'shop_id', 'owner', 'shop_name', 'shop_slug', 'city', 'state',
            'country', 'address', 'zip_code', 'phone', 'email',
            'description', 'logo_url', 'banner_url', 'status',
            'approval_date', 'commission_rate', 'created_at', 'updated_at'
        ]

class ShopDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopShopdocument # <-- Use the correct name
        fields = '__all__'

class ShopAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopShopattachment # <-- Use the correct name
        fields = '__all__'
