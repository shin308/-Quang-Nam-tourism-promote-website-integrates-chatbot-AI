# Generated by Django 3.0.4 on 2022-12-12 17:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0017_auto_20221213_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('place_id', models.AutoField(primary_key=True, serialize=False)),
                ('district', models.CharField(max_length=20)),
                ('price', models.IntegerField(default=20000)),
                ('rating', models.IntegerField(default=5)),
                ('dest_name', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=100)),
                ('img1', models.ImageField(upload_to='pics')),
                ('img2', models.ImageField(upload_to='pics')),
                ('img3', models.ImageField(upload_to='pics')),
                ('img4', models.ImageField(upload_to='pics')),
                ('img5', models.ImageField(upload_to='pics')),
                ('desc', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2022, 12, 12, 17, 51, 36, 688368, tzinfo=utc), max_length=19),
        ),
    ]
