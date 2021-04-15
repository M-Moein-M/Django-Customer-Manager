from accounts.models import Product


class ProductListAdmin:
	def __init__(self):
		self.products_list = Product.objects.all()

	def get_product_list(self):
		return self.products_list
