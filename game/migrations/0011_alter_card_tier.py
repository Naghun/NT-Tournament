# Generated by Django 4.2.2 on 2023-06-19 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_alter_card_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='tier',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1, null=True),
        ),
    ]
