# Generated by Django 3.0.4 on 2023-01-11 15:21

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travello', '0042_auto_20230111_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myrating',
            name='time_rate',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 15, 20, 59, 399091, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2023, 1, 11, 15, 20, 59, 395104, tzinfo=utc), max_length=19),
        ),
        migrations.CreateModel(
            name='PlaceRating',
            fields=[
                ('rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('comment', models.CharField(default='Good!!!', max_length=200)),
                ('time_rate', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='travello.Places')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
