from oscar.app import Shop
from oscar.core.application import Application

class SosciShop(Shop):

    # Override the core dashboard_app instance to use a blank application
    # instance.  This means no dashboard URLs are included.
    shipping_app = Application()
    offer_app = Application()


application = SosciShop()