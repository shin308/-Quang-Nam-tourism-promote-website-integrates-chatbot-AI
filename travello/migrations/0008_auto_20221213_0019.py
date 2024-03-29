# Generated by Django 3.0.4 on 2022-12-12 17:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0007_auto_20221101_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('place_id', models.AutoField(primary_key=True, serialize=False)),
                ('district', models.CharField(max_length=20)),
                ('price', models.IntegerField(default=20000)),
                ('rating', models.IntegerField(default=5)),
                ('dest_name', models.CharField(max_length=25)),
                ('img1', models.ImageField(upload_to='pics')),
                ('img2', models.ImageField(upload_to='pics')),
                ('img3', models.ImageField(upload_to='pics')),
                ('img4', models.ImageField(upload_to='pics')),
                ('img5', models.ImageField(upload_to='pics')),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('slide_id', models.AutoField(primary_key=True, serialize=False)),
                ('slide_image', models.ImageField(upload_to='pics')),
            ],
        ),
        migrations.AlterField(
            model_name='cards',
            name='Card_number',
            field=models.CharField(max_length=17, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cards',
            name='email',
            field=models.EmailField(default='thanhchau2279@gmail.com', max_length=50),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2022, 12, 12, 17, 19, 39, 582851, tzinfo=utc), max_length=19),
        ),
    ]
