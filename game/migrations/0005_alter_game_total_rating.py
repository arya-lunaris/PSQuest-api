# Generated by Django 4.2.19 on 2025-02-26 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_remove_game_age_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='total_rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
