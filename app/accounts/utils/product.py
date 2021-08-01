from ..forms import NewProductForm
from ..models import Tag, Product, Pack
from .img_file_upload import ImgFieldUploader


def replace_product_ins_with_subclass_ins(prod_list):
	res = []
	for i, prod in enumerate(prod_list):
		pack = Pack.objects.filter(id=prod.id)
		if pack:
			pack = pack[0]
			# used in template for rendering different bg
			setattr(pack, 'is_sub_of_product', True)
			res.append(pack)
		else:
			setattr(prod, 'is_sub_of_product', False)
			res.append(prod)
	return res


class SaveNewProduct:
	def __init__(self, request, edit_instance=None, form_class=NewProductForm):
		self.request = request
		self.product = None
		self.prod_form = form_class(
									self.request.POST,
									self.request.FILES,
									instance=edit_instance)

	def create_new_product(self):
		if self.prod_form.is_valid():
			self.save_new_product()

	def save_new_product(self):
		self.product = self.prod_form.save()
		self.save_product_pic_to_host()
		NewProductTagsManager(self.product, self.prod_form).save_tags()

	def save_product_pic_to_host(self):
		ImgFieldUploader(self.request.FILES, 'product_pic', self.product).save_pic()


class NewProductTagsManager:
	def __init__(self, product, product_form):
		self.product = product
		self.product_form = product_form
		self.product_tags = []

	def save_tags(self):
		tags = self.get_tags_list_from_form_data()
		for tag_name in tags:
			self.append_tag_to_product_tags_list(tag_name)
		self.update_product_tags()

	def get_tags_list_from_form_data(self):
		p_tags = self.product_form.cleaned_data.get('tags')
		return p_tags.split(',')

	def append_tag_to_product_tags_list(self, tag_name):
		t = ProductTag(tag_name)
		if t.is_tag_valid():
			self.product_tags.append(t.tag_obj)

	def update_product_tags(self):
		self.product.tags.clear()
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


class ProductDeleter:
	def __init__(self, pk):
		self.pk = pk

	def delete_product(self):
		Product.objects.filter(id=self.pk).delete()
