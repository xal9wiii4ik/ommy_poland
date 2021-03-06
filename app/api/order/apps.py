from django.apps import AppConfig

from django.db.models.signals import m2m_changed, post_save


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.order'

    def ready(self) -> None:
        from api.order.signals import remove_stores_from_user_managed_groups, creating_commission
        from api.order.models import Order

        m2m_changed.connect(remove_stores_from_user_managed_groups, sender=Order.master.through)
        post_save.connect(creating_commission, sender=Order)
