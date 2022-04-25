from rest_framework import serializers

from api.account.serializers import UserRegisterSerializer
from api.master.models import Master, MasterExperience, WorkSphere


class MasterExperienceModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model MasterExperience
    """

    class Meta:
        model = MasterExperience
        fields = '__all__'
        read_only_fields = ['master']


class MasterRegisterSerializer(UserRegisterSerializer):
    """
    Serializer for register master
    """

    master_experience = MasterExperienceModelSerializer(many=True, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    city = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    middle_name = serializers.CharField(max_length=100, required=True)


class MasterModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model master
    """

    class Meta:
        model = Master
        fields = '__all__'


class WorkSphereModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model work sphere
    """

    class Meta:
        model = WorkSphere
        fields = '__all__'
