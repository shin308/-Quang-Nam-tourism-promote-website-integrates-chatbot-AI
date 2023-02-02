# Generated by Django 3.0.4 on 2022-11-01 15:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0005_netbanking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('Transactions_ID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=10)),
                ('Trip_same_id', models.IntegerField(default=1)),
                ('Amount', models.CharField(max_length=8)),
                ('Status', models.CharField(default='Failed', max_length=15)),
                ('Payment_method', models.CharField(blank=True, max_length=15)),
                ('Date_Time', models.CharField(default=datetime.datetime(2022, 11, 1, 15, 11, 58, 622, tzinfo=utc), max_length=19)),
            ],
        ),
    ]