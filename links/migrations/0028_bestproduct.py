# Generated by Django 2.0 on 2019-04-30 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0027_auto_20190410_0511'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('products', models.ManyToManyField(blank=True, to='links.Product')),
            ],
        ),
    ]
