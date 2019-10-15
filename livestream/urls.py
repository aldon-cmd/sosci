from django.conf.urls import url

from livestream import views

urlpatterns = [
    url(r'^start-session/(?P<course_id>\d+)$', views.StartSessionView.as_view(), name='start-session'),
    url(r'^end-session/(?P<course_id>\d+)$', views.EndSessionView.as_view(), name='end-session'),
    url(r'^room-status$', views.TwilioRoomStatusView.as_view(), name='twilio-room-status'),
    url(r'^room/host/(?P<course_id>\d+)$', views.TwilioRoomView.as_view(), name='twilio-room'),
    url(r'^room/participant/(?P<course_id>\d+)$', views.TwilioRoomParticipantView.as_view(), name='twilio-room-participant'),

    
]