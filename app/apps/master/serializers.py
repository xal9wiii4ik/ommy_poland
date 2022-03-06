from rest_framework import serializers

from apps.account.serializers import UserRegisterSerializer
from apps.master.models import Master


class MasterRegisterSerializer(UserRegisterSerializer):
    """
    Serializer for register master
    """

    work_experience = serializers.IntegerField(required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)


class MasterModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model master
    """

    class Meta:
        model = Master
        fields = '__all__'
