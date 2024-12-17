# Generated by Django 5.1.2 on 2024-11-01 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='status',
            field=models.CharField(blank=True, choices=[('not_started', 'Boshlanmagan'), ('started', 'Boshlangan'), ('passed', "O'tgan"), ('failed', 'Yiqilgan'), ('ended', 'Tugagan')], default='not_started', max_length=20, null=True),
        ),
    ]