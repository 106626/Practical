# Generated by Django 2.0.5 on 2018-12-04 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0006_auto_20181204_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fastfood',
            name='imgs',
        ),
        migrations.RemoveField(
            model_name='fastfood',
            name='imgs_1',
        ),
        migrations.AddField(
            model_name='fastfood',
            name='StudentToken',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]
