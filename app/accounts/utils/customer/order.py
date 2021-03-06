from accounts.forms import NewOrderForm
from accounts.models import Customer, Product, Order
from ..order import ListOrders


class NewOrderCustomer:
	def __init__(self, request, pk):
		customer_id = request.user.customer.id
		self.quantity = self.get_order_quantity_from_form_data(request)
		self.customer = Customer.objects.get(id=customer_id)
		self.product = Product.objects.get(id=pk)

	def save_order(self):
		order = self.create_order_or_increment_quantity()
		order.save()

	def create_order_or_increment_quantity(self):
		try:
			return self.try_to_increment_quantity()
		except Order.DoesNotExist:
			return self.create_new_order_object()

	def try_to_increment_quantity(self):
		order = Order.objects.get(customer=self.customer.id,
								  product=self.product.id,
								  status='Pending')
		order.quantity += self.quantity
		return order

	def get_order_quantity_from_form_data(self, request):
		form = NewOrderForm(request.POST)
		if form.is_valid():
			return form.cleaned_data.get('quantity')

	def create_new_order_object(self):
		return Order(customer=self.customer,
					 product=self.product,
					 status='Pending',
					 quantity=self.quantity)


class OrdersListCustomer(ListOrders):
	def __init__(self, request, page_num, customer_id):
		super().__init__(request, page_num)
		self.customer_id = int(customer_id)

	def get_orders(self):
		orders = self.filter.get_filtered_orders()
		customer_orders = filter(lambda order: str(order.customer.id)==str(self.customer_id),orders)
		return list(customer_orders)[self.first_order: self.last_order]
