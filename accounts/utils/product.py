from ..forms import NewProductForm
from ..models import Tag


def create_new_product(request):
	prodForm = NewProductForm(request.POST)
	new_prod = prodForm.save()
	p_tags = prodForm.cleaned_data.get('tags')
	add_tags_to_new_product(new_prod, p_tags)


def add_tags_to_new_product(new_prod, pTags):
	tags = pTags.split(',')
	for t in tags:
		t = t.strip()
		if not t:
			continue
		new_tag = find_or_create_tag(tag_name=t)
		new_prod.tags.add(new_tag)


def find_or_create_tag(tag_name):
	tag = Tag.objects.filter(name=tag_name)
	if bool(tag):
		return tag[0]
	else:
		new_tag = Tag(name=tag_name)
		new_tag.save()
		return new_tag
