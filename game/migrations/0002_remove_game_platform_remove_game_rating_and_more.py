# Generated by Django 4.2.19 on 2025-02-24 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='platform',
        ),
        migrations.RemoveField(
            model_name='game',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='game',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='game',
            name='total_rating_count',
        ),
    ]
