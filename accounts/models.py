from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, null=True)
	phone = models.CharField(max_length=100, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	default_pfp = 'https://i.postimg.cc/8CsB3pgd/DEFAULTPROFILEPIC-VIwfo-SMcf7-IB2kd-I4y-Ka.png'
	profile_pic = models.CharField(max_length=250, default=default_pfp)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=100, default='__')

	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY = (
		('Indoor', 'Indoor'),
		('Out Door', 'Out Door'),
	)

	name = models.CharField(max_length=100, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=100, null=True, choices=CATEGORY)
	description = models.CharField(max_length=1023, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)
	product_pic = models.CharField(max_length=250, default='https://i.ibb.co/6nTkL30/Unknown-Product.png')

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
		('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered', 'Delivered')
	)

	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	status = models.CharField(max_length=100, choices=STATUS)
	quantity = models.IntegerField(default=1)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return f'{self.product.name} x {self.quantity}'
