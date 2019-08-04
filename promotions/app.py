from django.conf.urls import url
from oscar.apps.promotions import app
from promotions import views

class PromotionsApplication(app.PromotionsApplication):

    def get_urls(self):
    	
        urlpatterns = [
            url(r'^$', views.LandingView.as_view(), name='home'),
        ]
        urlpatterns += super(PromotionsApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)

application = PromotionsApplication()