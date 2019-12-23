from django.conf.urls import url

from video import views

app_name = 'video'

urlpatterns = [
    url(r'^upload/(?P<course_id>\d+)/$', views.VimeoVideoUploadFormView.as_view(), name='video-upload-form'),
    url(r'^upload/attempt/(?P<course_id>\d+)/$', views.VimeoVideoUploadAttemptView.as_view(), name='video-upload-attempt'),
    url(r'^player/(?P<course_id>\d+)/(?P<video_id>\d+)/$', views.VideoPlayerView.as_view(), name='play-video'),
    url(r'^player/(?P<course_id>\d+)/$', views.VideoPlayerView.as_view(), name='video-player'),    
    url(r'^list/(?P<course_id>\d+)/$', views.VideoListView.as_view(), name='video-list'),
]