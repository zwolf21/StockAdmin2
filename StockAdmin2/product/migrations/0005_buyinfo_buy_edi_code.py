# Generated by Django 2.0 on 2017-12-19 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20171219_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyinfo',
            name='buy_edi_code',
            field=models.CharField(blank=True, max_length=50, verbose_name='보험코드'),
        ),
    ]
