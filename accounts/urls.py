from accounts import views
from django.urls import path

app_name = 'accounts'

urlpatterns = (
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'register/',
        views.RegisterView.as_view(),
        name='register'
    ),
    path(
        'orders/',
        views.OrdersView.as_view(),
        name='orders'
    ),
    path(
        'activate/<str:token>/',
        views.ActivateView.as_view(),
        name='activate'
    ),
    path(
        'password_reset/',
        views.PasswordResetView.as_view(),
        name='password_reset'),
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    )
)
