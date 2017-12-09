# Generated by Django 2.0 on 2017-12-09 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, unique=True, verbose_name='구매번호')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='구매일자')),
                ('iscart', models.BooleanField(default=False, verbose_name='카트인지')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('commiter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '구매요청서',
                'verbose_name_plural': '구매요청서',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='BuyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='구매수량')),
                ('comment', models.CharField(blank=True, max_length=50, verbose_name='비고')),
                ('isend', models.BooleanField(default=False, verbose_name='구매종결')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('buy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='buy.Buy')),
                ('buyinfo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.BuyInfo')),
            ],
            options={
                'verbose_name': '구매품목',
                'verbose_name_plural': '구매품목',
            },
        ),
        migrations.AlterUniqueTogether(
            name='buyitem',
            unique_together={('buy', 'buyinfo')},
        ),
    ]
