# Generated by Django 5.0.6 on 2024-05-28 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineList',
            fields=[
                ('medicine_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id of medicines')),
                ('medicine_name', models.CharField(max_length=50, verbose_name='name of the medicine')),
            ],
        ),
    ]