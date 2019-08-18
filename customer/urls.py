from django.conf.urls import url
from customer import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(),name='login'),
    url(r'^login/modal$', views.LoginModalView.as_view(),name='login-modal'), 
    url(r'^logout$', views.LogoutView.as_view(),name='logout'),
    url(r'^registration$', views.UserRegistrationView.as_view(),name='user-registration'),
    url(r'^registration/modal$', views.RegistrationModalView.as_view(),name='registration-modal'),
    # url(r'^customer/(?P<pk>[0-9]+)/$', CustomerView.as_view(),name='customer-edit'),   
]