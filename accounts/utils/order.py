from ..models import Customer, Product, Order
from ..forms import NewOrderForm, UpdateOrderForm, OrderFilterForm
import math


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
	orders_per_page = 7
	def __init__(self, request, page_num):
		self.filter = FilterOrders(request)
		p = int(page_num)
		p = p if p > 0 else 1
		self.set_first_and_last_index(p)

	def set_first_and_last_index(self, page):
		self.first_order = self.orders_per_page * (page - 1)
		self.last_order = self.first_order + self.orders_per_page

	def get_orders(self):
		return self.filter.get_filtered_orders()

	def count_pages(self):
		return self.filter.count_pages()


class FilterOrders:
	def __init__(self, request):
		self.request = request

		self.query_dict = request.GET.dict()
		if not self.query_dict:
			self.filtered = Order.objects.all()
		else:
			prod_name = [x.strip() for x in self.query_dict.get('product_name', '').split(',')]
			del self.query_dict['product_name']
			del self.query_dict['submit']
			if any(prod_name):
				self.query_dict['product__name__in'] = prod_name
			self.filtered = Order.objects.filter(**self.query_dict)

	def get_filtered_orders(self):
		return self.filtered

	def count_pages(self):
		return math.ceil(len(self.filtered)/ListOrders.orders_per_page)
