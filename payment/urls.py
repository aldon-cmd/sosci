from django.conf.urls import url
from payment import views


urlpatterns = [
    url(r'^settle-pnp-payment/$', views.SettlePlugnPayPaymentView.as_view(), name='settle-pnp-payment'),
]

