# Generated by Django 4.0.6 on 2022-08-03 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formpage',
            name='thank_you_text',
            field=models.CharField(max_length=255),
        ),
    ]
