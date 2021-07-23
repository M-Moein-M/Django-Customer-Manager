from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
	if created:
		if instance.is_staff:
			add_group(instance, 'admin')
		else:
			add_group(instance, 'customer')


def add_group(instance, group_name):
	group = Group.objects.get(name=group_name)
	instance.groups.add(group)
	Customer.objects.create(user=instance, name=instance.username)

post_save.connect(customer_profile, sender=User)
