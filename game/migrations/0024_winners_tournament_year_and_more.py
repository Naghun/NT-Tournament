# Generated by Django 4.2.2 on 2023-07-09 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0023_alter_winners_tournament_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='winners',
            name='tournament_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='winners',
            name='tournament_number',
            field=models.BigIntegerField(default=0),
        ),
    ]
