import typing as tp

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe, SafeString

from api.order.models import Order, OrderFile


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    """
    Display model Order in admin panel
    """

    @staticmethod
    def display_work_sphere_name(obj: Order) -> str:
        """
        Display work sphere name
        Args:
            obj: current obj of Order
        Returns:
            name of work sphere
        """

        if obj.work_sphere is not None:
            return obj.work_sphere.name
        return 'Work sphere was remove'

    list_display = ('pk', 'name', 'description', 'customer',
                    'start_time', 'price', 'address',
                    'date_created', 'status',
                    'display_work_sphere_name', 'longitude', 'latitude')


@admin.register(OrderFile)
class OrderFileModelAdmin(admin.ModelAdmin):
    """
    Display model OrderFile in admin panel
    """

    @staticmethod
    def display_file(obj: OrderFile) -> tp.Union[SafeString, str]:
        """
        Display file on admin panel
        Args:
            obj: current obj of OrderImage
        Returns:
            SafeString: class which display html in admin panel
        """

        return mark_safe(f'<img src="{obj.bucket_path}" width="80" height="80" />')

    @staticmethod
    def move_to_order(obj: OrderFile) -> SafeString:
        """
        Link for move to edit or check info about current order
        Args:
            obj: current obj of OrderFile
        Returns:
            SafeString: class which display html in admin panel
        """

        link = reverse('admin:order_order_change', args=[obj.order.pk])
        return format_html(f'<a href="{link}">{obj.order.name}</a>')

    list_display = ('pk', 'move_to_order', 'display_file')
