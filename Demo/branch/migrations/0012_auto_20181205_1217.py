# Generated by Django 2.0.5 on 2018-12-05 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0011_bill_get'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='Get',
            field=models.CharField(default='0', max_length=2),
        ),
    ]
