import oscar.apps.customer.apps as apps
from django.conf.urls import url
from django.urls import re_path

class CustomerConfig(apps.CustomerConfig):
    name = 'customer'

    def ready(self):
        super().ready()
        #https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.ready
        from customer import views as customer_views
        self.customer_views = customer_views        

    def get_urls(self):        
	    
	    urls = [
                   re_path(r'^user-plan/list/$', self.customer_views.UserPlanListView.as_view(), name='user-plan-list'),
			       re_path(r'^students/invite/modal/$', self.customer_views.BulkStudentInviteModalView.as_view(), name='bulk-student-invite-modal'),				   
			       re_path(r'^student/invite/modal/$', self.customer_views.IndividualStudentInviteModalView.as_view(), name='individual-student-invite-modal'),
                   re_path(r'^student/list/$', self.customer_views.StudentListView.as_view(), name='student-list'),

	                url(r'^login/$', self.customer_views.LoginView.as_view(),name='user-login'),
	                url(r'^login/modal/(?P<course_id>\d+)/$', self.customer_views.LoginModalView.as_view(),name='login-modal'), 
	                url(r'^logout/$', self.customer_views.LogoutView.as_view(),name='logout'),
	                url(r'^registration/$', self.customer_views.UserRegistrationView.as_view(),name='user-registration'),
	                url(r'^registration/modal/(?P<course_id>\d+)/$', self.customer_views.RegistrationModalView.as_view(),name='registration-modal'),
	                url(r'^confirmation/resend/$', 
	                    self.customer_views.ResendUserEmailConfirmationView.as_view(),name='resend-email-confirmation'),            
	                url(r'^confirm/(?P<activation_key>\w+)/$', 
	                    self.customer_views.ConfirmUser.as_view(),name='confirm-user'),
	                url(r'^confirmation/sent/$', 
	                    self.customer_views.UserEmailConfirmationSentView.as_view(),name='email-confirmation-sent'),                
	                url(r'^password_reset/done/$', self.customer_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	                url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', self.customer_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	                url(r'^reset/done/$', self.customer_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	                url(r'^password_reset/$', self.customer_views.PasswordResetView.as_view(), name='password_reset'),                        
	        ]
	    urls += super().get_urls()

	    return self.post_process_urls(urls)    