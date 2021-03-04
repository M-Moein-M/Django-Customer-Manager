from ..forms import NewProductForm
from ..models import Tag
from .img_file_upload import ImgFieldUpload


class SaveNewProduct:
	def __init__(self, request):
		self.request = request
		self.product = None
		self.product_tags = []

	def create_new_product(self):
		prodForm = NewProductForm(self.request.POST, self.request.FILES)
		if prodForm.is_valid():
			self.product = prodForm.save()
			ImgFieldUpload(self.request.FILES, 'product_pic', self.product).save_pic()
			p_tags = prodForm.cleaned_data.get('tags')
			self.add_all_tags_to_new_product(p_tags)
		else:
			print(f'** {prodForm.errors} **')

	def add_all_tags_to_new_product(self, p_tags):
		tags = p_tags.split(',')
		for tag_name in tags:
			t = ProductTag(tag_name)
			if t.is_tag_valid():
				self.product_tags.append(t.tag_obj)

		self.save_added_tags_to_product()

	def save_added_tags_to_product(self):
		print(f'product tags:	{self.product_tags}')
		for t in self.product_tags:
			self.product.tags.add(t)
		# self.product.tags.add(*self.product_tags)


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
