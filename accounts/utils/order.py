from ..models import Customer, Product, Order
from ..forms import NewOrderForm, UpdateOrderForm


class SaveNewOrder:
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

class UpdateOrder:
	def __init__(self, request, order_instance):
		self.request = request
		self.instance = order_instance

	def update_order(self):
		form = UpdateOrderForm(self.request.POST, instance=self.instance)
		if form.is_valid():
			form.save()

class ListOrders:
	orders_per_page = 3
	def __init__(self, page_num):
		p = int(page_num)
		p = p if p > 0 else 1
		self.set_first_and_last_index(p)

	def set_first_and_last_index(self, page):
		self.first_order = self.orders_per_page * (page - 1)
		self.last_order = self.first_order + self.orders_per_page

	def get_orders(self):
		orders = Order.objects.order_by('date_created')[self.first_order: self.last_order]
		return orders

	@staticmethod
	def count_pages():
		return Order.objects.count()
