# Generated by Django 3.1.6 on 2021-03-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='/DEFAULTPROFILEPIC_VIwfoSMcf7IB2kdI4yKa.svg', null=True, upload_to=''),
        ),
    ]
