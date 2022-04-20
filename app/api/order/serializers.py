from rest_framework import serializers

from api.master.models import Master
from api.order.models import Order, OrderFile


class OrderImageModelSerializer(serializers.ModelSerializer):
    """ Model serializer for model order_file """

    class Meta:
        model = OrderFile
        fields = ['bucket_path']


class OrderMasterModelSerializer(serializers.ModelSerializer):
    """ Model serializer for order masters """

    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_full_name(master: Master):
        first_name = master.user.first_name
        last_name = master.user.last_name
        return f'{first_name} {last_name}'

    class Meta:
        model = Master
        fields = ['phone_number', 'full_name']


class OrderModelSerializer(serializers.ModelSerializer):
    """ Model Serializer for model Order """

    order_files = OrderImageModelSerializer(many=True, read_only=True)
    city = serializers.CharField(max_length=100, write_only=True)
    customer_name = serializers.CharField(read_only=True)
    customer_phone_number = serializers.CharField(read_only=True)
    master = OrderMasterModelSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['customer', 'date_created', 'master']


class GoogleSheetOrderSerializer(serializers.ModelSerializer):
    """ Model serializer for uploading order to google sheet """

    phone_number = serializers.CharField(max_length=13, read_only=True)
    work_sphere_name = serializers.CharField(max_length=13, read_only=True)
    order_files = OrderImageModelSerializer(many=True, read_only=True)
    commission = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Order
        fields = ['date_created', 'phone_number', 'work_sphere_name',
                  'number_employees', 'desired_time_end_work', 'start_time',
                  'address', 'description', 'order_files',
                  'status', 'price', 'commission']
