# Generated by Django 4.0.3 on 2022-03-13 06:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_delivery_creation_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 13, 6, 5, 54, 72635)),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='order_id',
            field=models.BigIntegerField(),
        ),
    ]
