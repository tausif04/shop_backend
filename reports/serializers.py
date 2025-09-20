from rest_framework import serializers
from .models import Report
from users.serializers import UserSerializer

class ReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
