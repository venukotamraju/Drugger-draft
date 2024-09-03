# Generated by Django 5.0.6 on 2024-05-28 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_vendordetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorCredentials',
            fields=[
                ('vendor_id', models.OneToOneField(db_column='vendor_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vendors.vendorlist')),
                ('vendor_email', models.CharField(max_length=30, verbose_name="vendor's email address")),
                ('vendor_key', models.CharField(max_length=30, verbose_name="vendor's password")),
            ],
        ),
    ]