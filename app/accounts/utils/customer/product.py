from accounts.models import Product, Pack
from accounts.utils.product import replace_product_ins_with_subclass_ins


class ProductListCustomer:
	def __init__(self):
		self.products_list = Product.objects.filter(availability='Available')

	def get_product_list(self):
		return replace_product_ins_with_subclass_ins(self.products_list)
