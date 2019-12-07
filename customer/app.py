from django.conf.urls import url
from oscar.apps.customer import app
from customer import views

class CustomerApplication(app.CustomerApplication):

    def get_urls(self):
    	
        urlpatterns = [
                url(r'^login/$', views.LoginView.as_view(),name='user-login'),
                url(r'^login/modal/(?P<course_id>\d+)/$', views.LoginModalView.as_view(),name='login-modal'), 
                url(r'^logout/$', views.LogoutView.as_view(),name='logout'),
                url(r'^registration/$', views.UserRegistrationView.as_view(),name='user-registration'),
                url(r'^registration/modal/(?P<course_id>\d+)/$', views.RegistrationModalView.as_view(),name='registration-modal'),
                url(r'^confirm/user/(?P<resend>\w+)/$', 
                    views.ConfirmUser.as_view(),name='resend-confirm-user'),            
                url(r'^confirm/(?P<activation_key>\w+)/$', 
                    views.ConfirmUser.as_view(),name='confirm-user'),
                url(r'^confirm/$', 
                    views.ConfirmUser.as_view(),name='email-confirm-user'),                
                url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
                url(r'^reset/done/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
                url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),                        
        ]
        urlpatterns += super(CustomerApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)

application = CustomerApplication()