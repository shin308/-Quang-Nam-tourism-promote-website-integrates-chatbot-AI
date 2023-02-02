# Generated by Django 3.0.4 on 2022-11-01 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0003_pessanger_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('Card_number', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('Ex_month', models.CharField(max_length=2)),
                ('Ex_Year', models.CharField(max_length=2)),
                ('CVV', models.CharField(max_length=3)),
                ('Balance', models.CharField(max_length=8)),
                ('email', models.EmailField(default='rambarodavala21@gmail.com', max_length=50)),
            ],
        ),
    ]
