# Generated by Django 3.0.4 on 2023-01-12 13:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0047_auto_20230112_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailed_desc',
            name='trip_date',
            field=models.DateField(default='2022-01-01'),
        ),
        migrations.AlterField(
            model_name='myrating',
            name='time_rate',
            field=models.DateField(default=datetime.datetime(2023, 1, 12, 13, 9, 1, 576767, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2023, 1, 12, 13, 9, 1, 576767, tzinfo=utc), max_length=19),
        ),
    ]
