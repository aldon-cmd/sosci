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
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from customer import models as customer_models


class VideoPlayerView(TemplateView):
    template_name = "video/player.html"

    def get_context_data(self, **kwargs):
        context = super(VideoPlayerView, self).get_context_data(**kwargs)
        video_id = self.kwargs.get("video_id")
        context['object'] = models.Video.objects.filter(pk=video_id).first()
        return context

class CourseListView(ListView):
    template_name = "video/course_list.html"
    paginate_by = 10
    model = models.Course

class CourseCreateView(CreateView):
    template_name = "video/course_form.html"
    model = models.Course
    fields = ['name']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('video:course-list')

class VideoListView(ListView):
    template_name = "video/video_list.html"
    paginate_by = 10
    model = models.Video

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return models.Video.objects.filter(course_id=course_id, course__user_id=self.request.user.pk)

class VimeoVideoUploadFormView(TemplateView):
    template_name = "video/vimeo_upload.html"

class VimeoVideoCreateView(View):

    def post(self, request, *args, **kwargs):

        post_data = request.POST
        course_id = self.kwargs.get("course_id")

        course = get_object_or_404(models.Course, pk=course_id,user_id=self.request.user.pk)

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

        try:
           response = requests.post(settings.VIMEO_CREATE_VIDEO_URL, json=data, headers=headers)

           json_response = response.json()

           try:
              video_id = int(json_response['uri'].split('/')[2])
           except ValueError:
                  pass

           models.Video.objects.create(name=json_response['name'],description=json_response['description'],video_id=video_id,width=json_response['width'],height=json_response['height'],duration=json_response['duration'],picture=json_response['pictures']['sizes'][2]['link_with_play_button'],upload_link=json_response['upload']['upload_link'],upload_status=json_response['upload']['status'],transcode_status=json_response['transcode']['status'],course_id=course_id)

           if not course.picture:
            #set the initial preview image of the course
             course.picture = json_response['pictures']['sizes'][2]['link_with_play_button']
             course.save()

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

        return JsonResponse(response.json())
