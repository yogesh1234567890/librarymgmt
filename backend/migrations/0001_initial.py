# Generated by Django 3.1.5 on 2021-01-19 11:32

import backend.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookEntry',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('summary', models.TextField(help_text='Enter a brief description of the book', max_length=1000)),
                ('isbn', models.IntegerField(help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', primary_key=True, serialize=False)),
                ('genre', models.TextField(help_text='For example: science, History, Technical, Enclyclopedia, etc.', max_length=20, null=True)),
                ('language', models.TextField(max_length=20)),
                ('total_copies', models.IntegerField()),
                ('available_copies', models.IntegerField()),
                ('pic', models.ImageField(blank=True, null=True, upload_to='book_image')),
                ('published_year', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Book Entry',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('avatar', models.ImageField(blank=True, default='avatar.jpg', upload_to='avatar/')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_book_name', models.CharField(max_length=200)),
                ('member_name', models.CharField(max_length=200)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('expirydate', models.DateField(default=backend.models.get_expiry)),
                ('isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.bookentry')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.member')),
            ],
            options={
                'verbose_name_plural': 'Book Issue',
            },
        ),
    ]
