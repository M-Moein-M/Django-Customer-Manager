from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, null=True)
	phone = models.CharField(max_length=100, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default='/DEFAULTPROFILEPIC_VIwfoSMcf7IB2kdI4yKa.svg', null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name or '**UNKNOWN**'


class Tag(models.Model):
	name = models.CharField(max_length=100, null=True)

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
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=100, choices=STATUS)

	def __str__(self):
		return self.product.name
