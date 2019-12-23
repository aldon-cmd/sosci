"""sosci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.apps import apps
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('instructor/', include('instructor.urls')),
    path('video/', include('video.urls')),
    path('live/', include('livestream.urls')),
    path('payment/', include('payment.urls')),
    path('admin/', admin.site.urls),
    path('', include(apps.get_app_config('shop').urls[0])),

]
