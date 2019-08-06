from decimal import Decimal as D
from django.db.transaction import atomic    
from partner.models import Partner, StockRecord 
from catalogue.models import ProductClass, Product, Category, ProductCategory
from oscar.apps.catalogue.categories import create_from_breadcrumbs

class CatalogueCreator(object):

    @atomic
    def create_product(self, product_class, category_str, title,
                     description,price_excl_tax, num_in_stock):

        item = self._create_item(product_class, category_str, title,
                     description)

        self._create_stockrecord(item,
                            price_excl_tax, num_in_stock)

    def _create_item(self, product_class, category_str, title,
                     description):

        # Create item class and item
        product_class, __ \
            = ProductClass.objects.get_or_create(name=product_class)

        item = Product()
        item.title = title
        item.description = description
        item.product_class = product_class
        item.save()

        # Category
        cat = create_from_breadcrumbs(category_str)
        ProductCategory.objects.update_or_create(product=item, category=cat)

        return item

    def _create_stockrecord(self, item,
                            price_excl_tax, num_in_stock):
        # Create partner and stock record
        partner_name = "Nesberry"
        partner_sku = "1337"
        partner, _ = Partner.objects.get_or_create(
            name=partner_name)
        try:
            stock = StockRecord.objects.get(partner_sku=partner_sku)
        except StockRecord.DoesNotExist:
            stock = StockRecord()

        stock.product = item
        stock.partner = partner
        stock.partner_sku = partner_sku
        stock.price_excl_tax = D(price_excl_tax)
        stock.num_in_stock = num_in_stock
        stock.save()