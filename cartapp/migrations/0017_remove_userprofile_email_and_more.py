# Generated by Django 4.2.13 on 2024-07-02 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0016_remove_userprofile_mod_date_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
    ]
