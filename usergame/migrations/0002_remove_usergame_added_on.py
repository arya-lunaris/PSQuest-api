# Generated by Django 4.2.19 on 2025-02-26 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usergame', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergame',
            name='added_on',
        ),
    ]
