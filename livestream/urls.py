from django.conf.urls import url

from livestream import views

app_name = 'live'

urlpatterns = [
    url(r'^room/meet/$', views.JitsiMeetRoomView.as_view(), name='jitsi-meet-room'),
    url(r'^room/participant/(?P<course_id>\d+)/$', views.TwilioRoomParticipantView.as_view(), name='twilio-room-participant'),

    
]