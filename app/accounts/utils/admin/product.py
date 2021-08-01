from accounts.models import Product
from accounts.utils.product import replace_product_ins_with_subclass_ins


class ProductListAdmin:
	def __init__(self):
		self.products_list = Product.objects.all()

	def get_product_list(self):
		return replace_product_ins_with_subclass_ins(self.products_list)
