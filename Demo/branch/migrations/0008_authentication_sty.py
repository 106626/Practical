# Generated by Django 2.0.5 on 2018-12-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0007_auto_20181204_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='authentication',
            name='sty',
            field=models.CharField(default=0, max_length=3),
            preserve_default=False,
        ),
    ]