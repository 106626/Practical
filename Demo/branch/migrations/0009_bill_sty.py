# Generated by Django 2.0.5 on 2018-12-05 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0008_authentication_sty'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='sty',
            field=models.CharField(default='0', max_length=2),
        ),
    ]