# Generated by Django 4.0 on 2022-01-09 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0004_rename_pname_detailmodel_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
