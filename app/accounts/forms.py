import datetime
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
import pytz


class ProductManyToManyFieldForm(forms.Form):
	m2m_field = forms.MultipleChoiceField(required=False,
										  choices=[(p.id, p) for p in Pack.objects.all()],
										  label='Add To Packs')


class NewPackForm(ModelForm):
	class Meta:
		model = Pack
		exclude = ['tags', 'product_pic']

	tags = forms.CharField(max_length=250)
	product_pic = forms.ImageField(required=False)
	products = forms.ModelMultipleChoiceField(
		queryset=Product.objects.filter(availability='Available').order_by('-date_created'),
		widget=forms.SelectMultiple
	)


class UpdateOrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['status']


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user', 'profile_pic']

	email = forms.CharField(max_length=200)


class ProfilePictureForm(forms.Form):
	profile_pic = forms.ImageField()


class NewProductForm(ModelForm):
	class Meta:
		model = Product
		exclude = ['tags', 'product_pic']

	tags = forms.CharField(max_length=250)
	product_pic = forms.ImageField(required=False)


class NewOrderForm(forms.Form):
	quantity = forms.IntegerField(min_value=1)


class OrderFilterForm(forms.Form):
	product_name = forms.CharField(max_length=255, required=False)
	quantity_range = forms.CharField(max_length=31, required=False, label='Quantity range(like 2, 17)')
	status_any = 'Any'
	status_choices = tuple(list(Order.STATUS)+[(status_any, 'Any')])
	status = forms.ChoiceField(choices=status_choices, required=False, initial=status_any)
	date_created_initial = forms.DateField(initial=datetime.datetime(2020, 1, 1, tzinfo=pytz.UTC))
	final_d = datetime.date.today()+datetime.timedelta(days=1)
	date_created_final = forms.DateField(initial=datetime.datetime(final_d.year, final_d.month, final_d.day, tzinfo=pytz.UTC))
