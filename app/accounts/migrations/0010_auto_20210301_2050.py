# Generated by Django 3.1.6 on 2021-03-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210301_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.CharField(default='https://i.postimg.cc/8CsB3pgd/DEFAULTPROFILEPIC-VIwfo-SMcf7-IB2kd-I4y-Ka.png', max_length=250),
        ),
    ]
