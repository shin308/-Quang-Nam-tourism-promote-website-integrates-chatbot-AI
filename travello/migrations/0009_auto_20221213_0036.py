# Generated by Django 3.0.4 on 2022-12-12 17:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0008_auto_20221213_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='dest_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2022, 12, 12, 17, 36, 48, 256553, tzinfo=utc), max_length=19),
        ),
    ]
