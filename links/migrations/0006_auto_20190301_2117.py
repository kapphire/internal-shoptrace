# Generated by Django 2.0 on 2019-03-01 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_auto_20190301_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
