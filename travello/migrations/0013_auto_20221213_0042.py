# Generated by Django 3.0.4 on 2022-12-12 17:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0012_auto_20221213_0042'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Places',
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2022, 12, 12, 17, 42, 47, 559523, tzinfo=utc), max_length=19),
        ),
    ]
