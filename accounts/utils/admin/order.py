from accounts.forms import UpdateOrderForm
from ..order import ListOrders


class OrderUpdate:
	def __init__(self, request, order_instance):
		self.request = request
		self.instance = order_instance

	def update_order(self):
		form = UpdateOrderForm(self.request.POST, instance=self.instance)
		if form.is_valid():
			form.save()


class OrdersListAdmin(ListOrders):
	def __init__(self, request, page_num):
		super().__init__(request, page_num)
