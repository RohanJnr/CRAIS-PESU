# Generated by Django 4.0.6 on 2022-09-10 04:59

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursefaculty',
            name='faculty',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.member'),
        ),
        migrations.AddField(
            model_name='coursefaculty',
            name='model',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='courses.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.courseprogram'),
        ),
    ]
