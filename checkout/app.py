from django.conf.urls import url
from oscar.apps.checkout import app
from checkout import views

class CheckoutApplication(app.CheckoutApplication):

    def get_urls(self):
    	
        urlpatterns = [
            url(r'payment-details/(?P<course_id>\d+)/$',
                views.PaymentDetailsView.as_view(), name='payment-details'),
            url(r'payment-details/$',
                views.PaymentDetailsView.as_view(), name='oscar-payment-details'),            
        ]
        urlpatterns += super(CheckoutApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)

application = CheckoutApplication()