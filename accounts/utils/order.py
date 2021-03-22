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
		self.set_first_and_last_index(page_num)

	def set_first_and_last_index(self, p):
		p = int(p)
		p = p if p > 0 else 1
		self.first_order = self.orders_per_page * (p - 1)
		self.last_order = self.first_order + self.orders_per_page

	def get_orders(self):
		return self.filter.get_filtered_orders()[self.first_order: self.last_order]

	def count_pages(self):
		return self.filter.count_pages()


class FilterOrders:
	def __init__(self, request):
		self.query_dict = request.GET.dict()
		self.apply_filter()

	def apply_filter(self):
		query_exists = bool(self.query_dict)
		if query_exists:
			self.adjust_query_dict_fields()
		self.filtered = Order.objects.filter(**self.query_dict).order_by('date_created')

	def adjust_query_dict_fields(self):
		OrderProductNameFilter(self.query_dict).adjust_query_dict()
		OrderQuantityRangeFilter(self.query_dict).adjust_query_dict()
		OrderStatusFilter(self.query_dict).adjust_query_dict()
		del self.query_dict['submit']

	def get_filtered_orders(self):
		return self.filtered

	def count_pages(self):
		return math.ceil(len(self.filtered)/ListOrders.orders_per_page)


class OrderFieldsFilter:
	def __init__(self, query_dict):
		self.query_dict = query_dict


class OrderStatusFilter(OrderFieldsFilter):
	def __init__(self, query_dict):
		super().__init__(query_dict)

	def adjust_query_dict(self):
		status = self.query_dict.get('status')
		if status == OrderFilterForm.status_any:
			del self.query_dict['status']


class OrderQuantityRangeFilter(OrderFieldsFilter):
	def __init__(self, query_dict):
		super().__init__(query_dict)

	def adjust_query_dict(self):
		self.set_quantity_range_in_query()
		del self.query_dict['quantity_range']

	def set_quantity_range_in_query(self):
		is_valid = self.validate_and_set_range()
		if is_valid:
			self.query_dict['quantity__gte'] = int(self.min_q)
			self.query_dict['quantity__lte'] = int(self.max_q)

	def validate_and_set_range(self):
		q_range = [x.strip() for x in self.query_dict.get('quantity_range', '').split(',')]
		if len(q_range) != 2:
			return False
		min_q, max_q = q_range
		if min_q.isdigit() and max_q.isdigit():
			self.min_q, self.max_q = min_q, max_q
			return True
		return False


class OrderProductNameFilter(OrderFieldsFilter):
	def __init__(self, query_dict):
		super().__init__(query_dict)

	def adjust_query_dict(self):
		prod_name = [x.strip() for x in self.query_dict.get('product_name', '').split(',')]
		del self.query_dict['product_name']
		if any(prod_name):
			self.query_dict['product__name__in'] = prod_name


class OrderDeleter:
	def __init__(self, order, status_condition='Pending'):
		self.order = order
		self.condition = status_condition

	def delete_order(self):
		if self.order.status == self.condition:
			self.order.delete()
			self.msg = 'Order Successfully Deleted'
			self.status = 'success'
		else:
			self.msg = f"You Can Delete Order If Only It's {self.condition}"
			self.status = 'error'

	def get_delete_status(self):
		return {
			'msg': self.msg,
			'status': self.status,
		}
