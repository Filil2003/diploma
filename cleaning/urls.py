from django.urls import path

from .views import HomeRedirectView, ServiceDetailView

app_name = 'cleaning'

urlpatterns = (
    path('', HomeRedirectView.as_view(), name='home'),
    path('cleaning/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
)
