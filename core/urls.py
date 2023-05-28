from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

handler400 = 'core.views.bad_request_view'
handler403 = 'core.views.permission_denied_view'
handler404 = 'core.views.page_not_found_view'
handler500 = 'core.views.server_error_view'

urlpatterns = [
    path('', include('cleaning.urls'), name='cleaning'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
