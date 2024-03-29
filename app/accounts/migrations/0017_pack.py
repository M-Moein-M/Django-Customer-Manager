# Generated by Django 3.1.13 on 2021-08-01 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_product_availability'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.product')),
                ('products', models.ManyToManyField(related_name='plist', to='accounts.Product')),
            ],
            bases=('accounts.product',),
        ),
    ]
