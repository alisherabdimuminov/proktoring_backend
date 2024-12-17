# Generated by Django 5.1.2 on 2024-12-14 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='position',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('student', 'Talaba')], max_length=20),
        ),
    ]
