# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests.exceptions import ConnectionError,HTTPError,ConnectTimeout,ReadTimeout,RequestException
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
# some_app/views.py
from django.views.generic import TemplateView
from django.views import View
from django.conf import settings
from video import models
from catalogue import models as catalogue_models
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import get_object_or_404
from catalogue.utils import Course
from django import http

class VideoPlayerView(TemplateView):
    template_name = "video/player.html"

    def dispatch(self, request, *args, **kwargs):

        course_id = self.kwargs.get('course_id')
        if not request.user.is_authenticated():
            return http.HttpResponseRedirect('/') 

        if not Course().is_enrolled(request.user,course_id):
            
            return http.HttpResponseRedirect(
                    reverse('catalogue:course-detail', kwargs={'course_id': course_id}))

        return super(VideoPlayerView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VideoPlayerView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        #display the first video in the playlist on page load
        video = models.Video.objects.filter(product_id=course_id).order_by('pk').first()
        if not video:
            raise http.Http404()
        context['video'] = video
        video_id = self.kwargs.get("video_id")
        #get video by id if a video_id is set in the url
        if video_id:        
            video = get_object_or_404(models.Video, video_id=video_id)

            context['video'] = video
        video.seen = True
        video.save()            
        context['videos'] = models.Video.objects.filter(product_id=course_id).exclude(pk=video.pk)
        return context

class VideoListView(ListView):
    template_name = "video/video_list.html"
    paginate_by = 10
    model = models.Video

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return models.Video.objects.filter(product_id=course_id)

class VimeoVideoUploadFormView(TemplateView):
    """
    this view displays an upload form
    """
    template_name = "video/vimeo_upload.html"

class VimeoVideoUploadAttemptView(View):
    """
    this view creates an upload attempt on the vimeo server
    """
    def post(self, request, *args, **kwargs):

        post_data = request.POST
        course_id = self.kwargs.get("course_id")

        course = get_object_or_404(catalogue_models.Product, pk=course_id,user_id=self.request.user.pk)

        headers = { 
                 'Authorization': 'bearer ' + settings.VIMEO_ACCESS_TOKEN,
                 'Content-Type': 'application/json',
                 'Accept': 'application/vnd.vimeo.*+json;version=3.4'
                  }

        data = {}

        data['upload'] = {
                'approach': 'tus',
                'size': post_data.get("file_size","")
            }

        video_creation_response = self.create_vimeo_video(settings.VIMEO_CREATE_VIDEO_URL,data,headers)

        try:
            video_id = int(video_creation_response['uri'].split('/')[2])
        except ValueError:
                pass

        name=video_creation_response['name']
        description=video_creation_response['description']
        video_id=video_id
        width=video_creation_response['width']
        height=video_creation_response['height']
        duration=video_creation_response['duration']
        picture=video_creation_response['pictures']['sizes'][2]['link_with_play_button']
        upload_link=video_creation_response['upload']['upload_link']
        upload_status=video_creation_response['upload']['status']
        transcode_status=video_creation_response['transcode']['status']
        course_id=course_id

        try:
           thumbnail_response = self.get_video_thumbnail(settings.VIMEO_GET_ALL_THUMBNAILS_URL.format(video_id),data,headers)
        except Exception as e:
            pass

        picture = thumbnail_response['sizes'][2]['link_with_play_button']

        module = self.create_course_module(post_data,course_id)

        models.Video.objects.create(name=name,description=description,video_id=video_id,width=width,height=height,duration=duration,picture=picture,upload_link=upload_link,upload_status=upload_status,transcode_status=transcode_status,module=module,product_id=course_id)

        if not course.picture:
        #set the initial preview image of the course
            course.picture = picture
            course.save()

        return JsonResponse(video_creation_response)

    def create_course_module(self,post_data,course_id):
        name = post_data.get("name","")
        # start_date = post_data.get("start_date","")

        module = catalogue_models.CourseModule.objects.create(name=name,product_id=course_id)
        return module

    def create_vimeo_video(self,url,data,headers):
        return self.make_request(url,data,headers)

    def get_video_thumbnail(self,url,data,headers):
        return self.make_request(url,data,headers)

    def make_request(self,url,data,headers):
        try:
            response = requests.post(url, json=data, headers=headers)

            json_response = response.json()

            return json_response

        except ConnectionError as e:
            return JsonResponse({'message':e.message}, status = 500)

        except (HTTPError,ConnectTimeout,ReadTimeout) as e:
            try:
                json_response = response.json()
            except Exception:
                pass

            if json_response:
                    message = json_response.get('error') or json_response.get('Description')
            elif hasattr(response, 'text'):
                response_message = getattr(response, 'message', 'There was an unexpected error.')
                message = getattr(response, 'text', response_message)
            else:
                message = getattr(response, 'message')

            return JsonResponse({'message':message}, status = 500)

        except RequestException as e:

            return JsonResponse({'message':e.message}, status = 500)

        except Exception as e:

            return JsonResponse({'message':e.message}, status = 500)