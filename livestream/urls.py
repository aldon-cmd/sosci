from django.conf.urls import url

from livestream import views

urlpatterns = [
    url(r'^room/(?P<course_id>\d+)$', views.TwilioRoomView.as_view(), name='twilio-room'),
]