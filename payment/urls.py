from django.conf.urls import url
from payment import views

app_name = 'payment'

urlpatterns = [
    url(r'^settle-pnp-payment/(?P<course_id>\d+)/$', views.SettlePlugnPayPaymentView.as_view(), name='settle-pnp-payment'),
]

