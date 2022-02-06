from rest_framework.routers import SimpleRouter

from apps.order.views import OrderCreateOnlyViewSet

posts_router = SimpleRouter()
posts_router.register(prefix=r'order', viewset=OrderCreateOnlyViewSet)

urlpatterns = posts_router.urls
