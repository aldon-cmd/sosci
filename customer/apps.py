import oscar.apps.customer.apps as apps
from django.conf.urls import url

class CustomerConfig(apps.CustomerConfig):
    name = 'customer'

    def ready(self):
        super().ready()
        #https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.ready
        from customer import views as customer_views
        self.customer_views = customer_views        

    def get_urls(self):        
	    
	    urls = [
	                url(r'^login/$', self.customer_views.LoginView.as_view(),name='user-login'),
	                url(r'^login/modal/(?P<course_id>\d+)/$', self.customer_views.LoginModalView.as_view(),name='login-modal'), 
	                url(r'^logout/$', self.customer_views.LogoutView.as_view(),name='logout'),
	                url(r'^registration/$', self.customer_views.UserRegistrationView.as_view(),name='user-registration'),
	                url(r'^registration/modal/(?P<course_id>\d+)/$', self.customer_views.RegistrationModalView.as_view(),name='registration-modal'),
	                url(r'^confirm/user/(?P<resend>\w+)/$', 
	                    self.customer_views.ConfirmUser.as_view(),name='resend-confirm-user'),            
	                url(r'^confirm/(?P<activation_key>\w+)/$', 
	                    self.customer_views.ConfirmUser.as_view(),name='confirm-user'),
	                url(r'^confirm/$', 
	                    self.customer_views.ConfirmUser.as_view(),name='email-confirm-user'),                
	                url(r'^password_reset/done/$', self.customer_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	                url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', self.customer_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	                url(r'^reset/done/$', self.customer_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	                url(r'^password_reset/$', self.customer_views.PasswordResetView.as_view(), name='password_reset'),                        
	        ]
	    urls += super().get_urls()

	    return self.post_process_urls(urls)    