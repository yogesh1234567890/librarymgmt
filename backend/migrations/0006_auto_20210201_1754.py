# Generated by Django 3.1.5 on 2021-02-01 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_bookrenew'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookentry',
            old_name='available_copies',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='bookentry',
            name='total_copies',
        ),
        migrations.AddField(
            model_name='bookentry',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]