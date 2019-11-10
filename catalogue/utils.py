from decimal import Decimal as D
from django.db.transaction import atomic    
from partner.models import Partner, StockRecord 
from catalogue import models as catalogue_models
from oscar.apps.catalogue.categories import create_from_breadcrumbs
from livestream import models as twilio_models

class Course(object):

    def get_course(self,course_id):
        return catalogue_models.Product.objects.prefetch_related("coursemodules").filter(pk=course_id).first()

class Enrollment(object):

      def enroll(self,user,course_id):
          catalogue_models.Enrollment.objects.get_or_create(product_id=course_id, user=user)

      def is_enrolled(self,user, course_id):
          return catalogue_models.Enrollment.objects.filter(user=user,product_id=course_id).exists()

class CatalogueCreator(object):

    @atomic
    def create_product(self,user, product_class, category_str, title,
                     description,price_excl_tax, num_in_stock):

        item = self._create_item(user,product_class, category_str, title,
                     description)

        self._create_stockrecord(item,
                            price_excl_tax, num_in_stock)
        return item

    def _create_item(self,user, product_class, category_str, title,
                     description):

        # Create item class and item
        product_class, __ \
            = catalogue_models.ProductClass.objects.get_or_create(name=product_class,requires_shipping=False,track_stock=False)

        item = catalogue_models.Product()
        item.user = user
        item.title = title
        item.description = description
        item.product_class = product_class
        item.save()

        self._create_room(item)

        # Category
        cat = create_from_breadcrumbs(category_str)
        catalogue_models.ProductCategory.objects.update_or_create(product=item, category=cat)

        return item

    def _create_stockrecord(self, item,
                            price_excl_tax, num_in_stock):
        # Create partner and stock record
        partner_name = "Nesberry"
        # partner_sku = "1337"
        partner, _ = Partner.objects.get_or_create(
            name=partner_name)

        stock = StockRecord()

        stock.product = item
        stock.partner = partner
        stock.partner_sku = item.pk
        stock.price_excl_tax = D(price_excl_tax)
        stock.num_in_stock = num_in_stock
        stock.save()

    def _create_room(self,product):
        twilio_models.TwilioRoom.objects.create(name=product.pk,product=product)