from django.conf.urls import url

from livestream import views

urlpatterns = [
    url(r'^room/participant/(?P<course_id>\d+)/$', views.TwilioRoomParticipantView.as_view(), name='twilio-room-participant'),

    
]