from ..forms import NewProductForm
from ..models import Tag
from .img_file_upload import ImgFieldUpload


class SaveNewProduct:
	def __init__(self, request):
		self.request = request
		self.product = None
		self.product_tags = []
		self.prod_form = NewProductForm(self.request.POST, self.request.FILES)

	def create_new_product(self):
		if self.prod_form.is_valid():
			self.save_new_product()

	def save_new_product(self):
		self.product = self.prod_form.save()
		self.save_product_pic_to_host()
		self.add_all_tags_to_new_product()

	def save_product_pic_to_host(self):
		ImgFieldUpload(self.request.FILES, 'product_pic', self.product).save_pic()

	def add_all_tags_to_new_product(self):
		tags = self.get_tags_list_from_form_data()
		for tag_name in tags:
			self.append_tag_to_product_tags_list(tag_name)
		self.save_added_tags_to_product()

	def get_tags_list_from_form_data(self):
		p_tags = self.prod_form.cleaned_data.get('tags')
		return p_tags.split(',')

	def append_tag_to_product_tags_list(self, tag_name):
		t = ProductTag(tag_name)
		if t.is_tag_valid():
			self.product_tags.append(t.tag_obj)

	def save_added_tags_to_product(self):
		self.product.tags.add(*self.product_tags)


class ProductTag:
	def __init__(self, tag_name):
		self.name = tag_name.strip()
		self.tag_obj = None
		self.find_or_create_tag()

	def is_tag_valid(self):
		is_not_empty = bool(self.name)
		return is_not_empty

	def find_or_create_tag(self):
		tag = Tag.objects.filter(name=self.name)
		does_exist = bool(tag)
		if does_exist:
			self.tag_obj = tag[0]
		else:
			self.tag_obj = self.craete_new_tag_obj()

	def craete_new_tag_obj(self):
		new_tag = Tag(name=self.name)
		new_tag.save()
		return new_tag
