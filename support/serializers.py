from rest_framework import serializers
from .models import SupportTicket
from users.serializers import UserSerializer

class SupportTicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SupportTicket
        fields = '__all__'
