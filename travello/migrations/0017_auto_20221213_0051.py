# Generated by Django 3.0.4 on 2022-12-12 17:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0016_auto_20221213_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2022, 12, 12, 17, 50, 58, 882016, tzinfo=utc), max_length=19),
        ),
    ]
