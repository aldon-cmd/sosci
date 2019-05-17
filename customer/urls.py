from django.conf.urls import url
from customer import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(),name='login'),
    url(r'^logout$', auth_views.LogoutView.as_view(),name='logout'),
    url(r'^registration$', views.UserRegistrationView.as_view(),name='user-registration'),
    # url(r'^customer/(?P<pk>[0-9]+)/$', CustomerView.as_view(),name='customer-edit'),   
]