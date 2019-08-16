"""sosci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# from course.views import CourseListView
# from promotions.views import LandingView
from app import application

urlpatterns = [
    url(r'^video/', include('video.urls', namespace='video')),
    # url(r'^promotions/', include('promotions.urls', namespace='promotions')),
    # url(r'^course/', include('course.urls', namespace='course')),
    url(r'^accounts/', include('customer.urls', namespace='customer')),
    url(r'^admin/', admin.site.urls),
    # url('^$', LandingView.as_view(), name='index')
    url(r'', include(application.urls)),

]
