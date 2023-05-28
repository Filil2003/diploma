from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = (
    path(
        'create/<slug:slug>/',
        views.OrderCreateWizardView.as_view(),
        name='create'
    ),
    path(
        'admin/order/<int:order_id>/',
        views.AdminOrderDetailView.as_view(),
        name='admin_order_detail'
    )
)
