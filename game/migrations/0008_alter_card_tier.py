# Generated by Django 4.2.2 on 2023-06-19 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_card_speed_card_tier_card_wins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='tier',
            field=models.IntegerField(blank=True, choices=[('Tier 1', 1), (2, 'Tier 2'), (3, 'Tier 3'), (4, 'Tier 4')], default=1, null=True),
        ),
    ]
