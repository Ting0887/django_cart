# Generated by Django 4.0 on 2022-01-09 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0007_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.BinaryField(),
        ),
    ]
