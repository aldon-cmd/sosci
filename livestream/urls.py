from django.conf.urls import url

from livestream import views

urlpatterns = [
    url(r'^token$', views.TwilioTokenView.as_view(), name='twilio-token'),
    url(r'^player$', views.TwilioPlayerView.as_view(), name='twilio-player'),

]