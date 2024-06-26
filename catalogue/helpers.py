from decimal import Decimal as D
from django.db.transaction import atomic    
from partner.models import Partner, StockRecord 
from catalogue import models as catalogue_models
from oscar.apps.catalogue.categories import create_from_breadcrumbs
from livestream import models as twilio_models

class Course(object):

    def exists(self, course_id):
        return catalogue_models.Product.objects.filter(pk=course_id).exists()

    def is_owner(self,course,user):
        return course.user == user

    def is_published(self,course_id):
        return catalogue_models.Product.objects.filter(pk=course_id,is_published=True).exists()

    def get_courses(self):
        return catalogue_models.Product.objects.select_related("product_class")

    def get_course(self,course_id):
        return catalogue_models.Product.objects.select_related("product_class","user").prefetch_related("coursemodules").filter(pk=course_id).first()

    def enroll(self,user,course_id):
        catalogue_models.Enrollment.objects.get_or_create(product_id=course_id, user=user)

    def is_enrolled(self,user, course_id):
        return user.is_authenticated and catalogue_models.Enrollment.objects.filter(user=user,product_id=course_id).exists()

class CatalogueCreator(object):

    @atomic
    def create_product(self,user, product_class, category_str, product,price_excl_tax, num_in_stock):

        item = self._create_item(user,product_class, category_str, product)

        self._create_stockrecord(item,
                            price_excl_tax, num_in_stock)
        return item

    def _create_item(self,user, product_class, category_str, product):

        # Create item class and item
        product_class, __ \
            = catalogue_models.ProductClass.objects.get_or_create(name=product_class,requires_shipping=False,track_stock=False)

        product.user = user
        product.product_class = product_class
        product.save()

        self._create_room(product)

        # Category
        cat = create_from_breadcrumbs(category_str)
        catalogue_models.ProductCategory.objects.update_or_create(product=product, category=cat)

        return product

    def _create_stockrecord(self, item,
                            price_excl_tax, num_in_stock):
        # Create partner and stock record
        partner_name = "Nesberry"

        partner = Partner.objects.filter(name=partner_name).first()

        stock = StockRecord()

        stock.product = item
        stock.partner = partner
        stock.partner_sku = item.pk
        stock.price_excl_tax = D(price_excl_tax)
        stock.num_in_stock = num_in_stock
        stock.save()

    def _create_room(self,product):
        twilio_models.TwilioRoom.objects.create(name=product.pk,product=product)