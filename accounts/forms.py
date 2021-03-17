from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


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
	product_name = forms.CharField(max_length=255)
