# Generated by Django 2.0 on 2017-12-15 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buy', '0005_auto_20171213_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyitem',
            name='buyinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.BuyInfo'),
        ),
        migrations.AlterField(
            model_name='stockrecord',
            name='buyitem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buy.BuyItem'),
        ),
    ]