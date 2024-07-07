# Generated by Django 4.2.13 on 2024-07-03 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0019_alter_userprofile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailmodel',
            old_name='customname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='ordermodel',
            old_name='customaddress',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='ordermodel',
            old_name='customemail',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='ordermodel',
            old_name='customname',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='detailmodel',
            name='unitprice',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='customphone',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='paytype',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='shipping',
        ),
    ]