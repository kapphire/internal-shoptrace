# Generated by Django 2.0 on 2019-03-21 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0023_auto_20190322_0333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='record',
        ),
        migrations.AddField(
            model_name='schedulerrecord',
            name='links',
            field=models.ManyToManyField(blank=True, to='links.Link'),
        ),
    ]
