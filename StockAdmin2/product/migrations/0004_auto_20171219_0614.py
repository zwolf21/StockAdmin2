# Generated by Django 2.0 on 2017-12-19 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20171219_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyinfo',
            name='edi_code',
        ),
        migrations.AddField(
            model_name='product',
            name='edi_code',
            field=models.CharField(blank=True, max_length=50, verbose_name='보험코드'),
        ),
        migrations.AlterField(
            model_name='buyinfo',
            name='market',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Market'),
        ),
    ]