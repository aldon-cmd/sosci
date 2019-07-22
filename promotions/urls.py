from django.conf.urls import url

from promotions import views

urlpatterns = [
    url(r'^landing$', views.LandingView.as_view(), name='landing'),
]