# Generated by Django 4.2.2 on 2023-07-05 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_card_crit_card_fatique'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitialCards',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('overall', models.PositiveIntegerField(default=0)),
                ('speed', models.IntegerField(blank=True, default=0, null=True)),
                ('health', models.PositiveIntegerField(default=0)),
                ('attack', models.PositiveIntegerField(default=0)),
                ('deffence', models.PositiveIntegerField(default=0)),
                ('wins', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament', models.PositiveIntegerField(default=1)),
                ('year', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Winners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.CharField(max_length=250)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.tournament')),
            ],
        ),
    ]
