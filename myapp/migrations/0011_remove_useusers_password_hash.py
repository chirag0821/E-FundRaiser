# Generated by Django 4.0.3 on 2022-03-15 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_rename_users_useusers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useusers',
            name='password_hash',
        ),
    ]
