# Generated by Django 2.0 on 2019-03-12 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0015_auto_20190306_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchedulerLookUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('number', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]