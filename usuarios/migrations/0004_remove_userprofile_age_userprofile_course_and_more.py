# Generated by Django 4.2.6 on 2023-11-20 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_rename_website_userprofile_github_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='course',
            field=models.CharField(blank=True, max_length=255, verbose_name='Course'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Phone'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website_url',
            field=models.URLField(blank=True, verbose_name='Website URL'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='github_url',
            field=models.URLField(blank=True, verbose_name='GitHub URL'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='instagram_url',
            field=models.URLField(blank=True, verbose_name='Instagram URL'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/', verbose_name='Profile Picture'),
        ),
    ]
