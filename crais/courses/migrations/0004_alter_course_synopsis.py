# Generated by Django 4.0.6 on 2022-08-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='synopsis',
            field=models.TextField(),
        ),
    ]
