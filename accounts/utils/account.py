from ..forms import CustomerForm
from .img_file_upload import ImgFieldUpload


def is_user_authorized_to_visit_page(req_user, authorized_id):
	if req_user.groups.all()[0].name == 'admin':
		return True
	else:
		return str(req_user.customer.id) == str(authorized_id)


class SaveCustomerSettings:
	def __init__(self, request):
		self.request = request

	def save_settings(self):
		self.customer = self.request.user.customer
		self.save_image_settings()
		self.save_info_settings()

	def save_info_settings(self):
		info = CustomerForm(self.request.POST, instance=self.customer)
		if info.is_valid():
			self.save_customer_info_data(info)

	def save_image_settings(self):
		ImgFieldUpload(self.request.FILES, 'profile_pic', self.customer).save_pic()

	def save_customer_info_data(self, info):
		customer = info.save()
		email = info.cleaned_data.get('email')
		if email != customer.user.email:
			self.save_user_new_email(customer, email)


	def save_user_new_email(self, customer, email):
		customer.user.email = email
		customer.user.save()
