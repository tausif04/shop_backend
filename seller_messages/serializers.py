from rest_framework import serializers
from .models import SellerMessage
from users.serializers import UserSerializer

class SellerMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = SellerMessage
        fields = '__all__'
