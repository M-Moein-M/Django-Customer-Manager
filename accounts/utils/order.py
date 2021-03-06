from ..models import Customer, Product, Order
from ..forms import NewOrderForm


class SaveNewOrder:
	def __init__(self, request, pk):
		customer_id = request.user.customer.id
		self.quantity = self.get_order_quantity_from_form_data(request)
		self.customer = Customer.objects.get(id=customer_id)
		self.product = Product.objects.get(id=pk)

	def save_order(self):
		order = self.get_order_object()
		order.save()

	def get_order_quantity_from_form_data(self, request):
		form = NewOrderForm(request.POST)
		if form.is_valid():
			return form.cleaned_data.get('quantity')

	def get_order_object(self):
		return Order(customer=self.customer,
					 product=self.product,
					 status='Pending',
					 quantity=self.quantity)
