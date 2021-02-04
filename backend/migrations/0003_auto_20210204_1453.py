# Generated by Django 3.1.5 on 2021-02-04 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20210204_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='last_name',
        ),
        migrations.AddField(
            model_name='member',
            name='full_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
