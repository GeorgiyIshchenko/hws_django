# Generated by Django 3.0.5 on 2020-06-28 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainhws', '0002_article_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
    ]