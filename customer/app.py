from django.conf.urls import url
from oscar.apps.customer import app
from customer import views

class CustomerApplication(app.CustomerApplication):

    def get_urls(self):
    	
        urlpatterns = [
                url(r'^login$', views.LoginView.as_view(),name='user-login'),
                url(r'^login/modal/(?P<course_id>\d+)/$', views.LoginModalView.as_view(),name='login-modal'), 
                url(r'^logout$', views.LogoutView.as_view(),name='logout'),
                url(r'^registration$', views.UserRegistrationView.as_view(),name='user-registration'),
                url(r'^registration/modal/(?P<course_id>\d+)/$', views.RegistrationModalView.as_view(),name='registration-modal'),        
        ]
        urlpatterns += super(CustomerApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)

application = CustomerApplication()