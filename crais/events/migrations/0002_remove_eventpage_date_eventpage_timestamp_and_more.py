# Generated by Django 4.0.6 on 2022-09-09 17:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='date',
        ),
        migrations.AddField(
            model_name='eventpage',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date and Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='venue',
            field=models.CharField(default='PES', max_length=255),
            preserve_default=False,
        ),
    ]
