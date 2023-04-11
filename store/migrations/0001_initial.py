# Generated by Django 4.1.2 on 2023-04-10 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('ProductID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('ProductName', models.CharField(max_length=255)),
                ('BrandName', models.CharField(max_length=25)),
                ('ShopName', models.CharField(max_length=20)),
                ('ImageLink', models.URLField(max_length=255)),
                ('ProductLink', models.URLField(max_length=255)),
                ('SalePrice', models.CharField(max_length=12)),
                ('NormalPrice', models.CharField(max_length=12)),
                ('Type', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Detail', models.CharField(max_length=255)),
                ('ProdID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FeatureName', models.CharField(max_length=50)),
                ('ProdID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ConfigName', models.CharField(max_length=50)),
                ('Detail', models.CharField(max_length=100)),
                ('ProdID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
