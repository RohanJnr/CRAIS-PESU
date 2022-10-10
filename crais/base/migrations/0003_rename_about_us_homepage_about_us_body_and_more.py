# Generated by Django 4.0.6 on 2022-10-07 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_formpage_general_information_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='about_us',
            new_name='about_us_body',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='image_1',
            new_name='about_us_image',
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_us_tagline',
            field=models.CharField(default='sd', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_us_title',
            field=models.CharField(default='title', max_length=32),
            preserve_default=False,
        ),
    ]