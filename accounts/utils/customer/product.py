from accounts.models import Product

class ProductListCustomer:
	def __init__(self):
		self.products_list = Product.objects.filter(availability='Available')

	def get_product_list(self):
		return self.products_list
