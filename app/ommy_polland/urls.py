from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ommy_polland.yasg import urlpatterns as doc_urls
from ommy_polland import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(('api.account.urls', 'account'), namespace='account')),
    path('api/', include(('api.order.urls', 'order'), namespace='order')),
    path('api/', include(('api.master.urls', 'master'), namespace='master')),
    path('api/', include(('api.authenticate.urls', 'authenticate'), namespace='authenticate')),
    path('api/', include(('api.payments.urls', 'authenticate'), namespace='payments')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
