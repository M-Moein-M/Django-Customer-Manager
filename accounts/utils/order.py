from ..models import Customer, Product, Order


class SaveNewOrder:
	def __init__(self, request, pk):
		customer_id = request.user.customer.id
		self.customer = Customer.objects.get(id=customer_id)
		self.product = Product.objects.get(id=pk)

	def save_order(self):
		Order(customer=self.customer,
			  product=self.product,
			  status='Pending').save()
