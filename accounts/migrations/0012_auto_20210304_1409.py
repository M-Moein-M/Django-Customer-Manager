# Generated by Django 3.1.6 on 2021-03-04 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210304_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_picture',
            new_name='product_pic',
        ),
    ]