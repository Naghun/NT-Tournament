# Generated by Django 4.2.2 on 2023-06-08 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='attack_game',
        ),
        migrations.RemoveField(
            model_name='card',
            name='deffence_game',
        ),
        migrations.RemoveField(
            model_name='card',
            name='health_game',
        ),
        migrations.RemoveField(
            model_name='card',
            name='overall_game',
        ),
        migrations.RemoveField(
            model_name='card',
            name='picture',
        ),
    ]