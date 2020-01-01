import oscar.apps.checkout.apps as apps
from django.urls import re_path


class CheckoutConfig(apps.CheckoutConfig):
    name = 'checkout'

    def ready(self):
        super().ready()
        #https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.ready
        from checkout import views as checkout_views
        self.checkout_views = checkout_views

    def get_urls(self):
        

        urls = [
            re_path(r'payment-details/(?P<course_id>\d+)/$',
                self.checkout_views.PaymentDetailsView.as_view(), name='payment-details'),
            re_path(r'payment-details/$',
                self.checkout_views.PaymentDetailsView.as_view(), name='oscar-payment-details'),
            re_path(r'thank-you/$', self.checkout_views.ThankYouView.as_view(),
                name='thank-you'),            
        ]

        urls += super().get_urls()

        return self.post_process_urls(urls)