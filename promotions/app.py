from django.conf.urls import url
from oscar.apps.promotions import app
from promotions import views

class PromotionsApplication(app.PromotionsApplication):

    def get_urls(self):
    	urlpatterns = super(PromotionsApplication, self).get_urls()
        urlpatterns += [
            url(r'^$', views.LandingView.as_view(), name='home'),
        ]
        return self.post_process_urls(urlpatterns)

application = PromotionsApplication()