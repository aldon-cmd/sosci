from oscar import config
from django.conf.urls import url

class SosciShopConfig(config.Shop):
    name = 'shop'

    def ready(self):
        super().ready()
        from shop import views as shop_views
        self.shop_views = shop_views

    def get_urls(self):
    	
        urls = [
            url(r'^welcome1/$', self.shop_views.Welcome1View.as_view(), name='welcome1'),
            url(r'^welcome2$', self.shop_views.Welcome2View.as_view(), name='welcome2'),
            url(r'^$', self.shop_views.LandingView.as_view(), name='home'),
        ]

        urls += super().get_urls()
        
        return self.post_process_urls(urls)