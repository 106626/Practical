# Generated by Django 2.0.5 on 2018-12-10 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0015_auto_20181209_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fastfood',
            name='imgs',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='fastfood',
            name='imgs_1',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
