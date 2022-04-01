from rest_framework import serializers

from api.order.models import Order, OrderFile


class OrderImageModelSerializer(serializers.ModelSerializer):
    """
    Model serializer for model order_file
    """

    file_url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = OrderFile
        fields = '__all__'


class OrderModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model Order
    """

    files = OrderImageModelSerializer(many=True, required=False)
    city = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['customer', 'date_created', 'master']
