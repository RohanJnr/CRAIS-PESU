# Generated by Django 4.2.2 on 2023-06-28 07:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('content', '0002_courseprogram_coursesindexpage_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'verbose_name': 'Member Category',
                'verbose_name_plural': 'Member Categories',
                'ordering': ('name',),
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('linkedin_link', models.URLField(blank=True, null=True)),
                ('google_scholar_link', models.URLField(blank=True, null=True)),
                ('pes_faculty_profile_link', models.URLField(blank=True, null=True)),
                ('srn', models.CharField(blank=True, help_text='Enter srn if applicable', max_length=32, null=True)),
                ('university', models.CharField(max_length=128)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.membercategory')),
                ('faculty_guide', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.member')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
        ),
    ]