from oscar.apps.basket.signals import basket_addition

class BasketMixin(object):

	def basket_add(self,request, basket,product):
	    basket.add_product(
	        product, 1)

	    # Send signal for basket addition
	    basket_addition.send(
	        sender=self, product=product, user=request.user,
	        request=request)