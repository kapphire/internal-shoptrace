# Generated by Django 2.0 on 2019-03-21 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0022_auto_20190322_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='record',
        ),
        migrations.AddField(
            model_name='link',
            name='record',
            field=models.ManyToManyField(blank=True, to='links.SchedulerRecord'),
        ),
    ]
