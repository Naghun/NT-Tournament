from django.db import models

# Create your models here.
class Card(models.Model):

    RACE = (
        ('Human', 'Human'),
        ('Fantasy', 'Fantasy'),
        ('Creature', 'Creature'),
        ('Alien', 'Alien'),
    )

    id=models.IntegerField(blank=True, primary_key=True)
    name=models.CharField(max_length=100)
    race=models.CharField(max_length=50, choices=RACE, default=None)
    overall=models.PositiveIntegerField(default=0)
    health=models.PositiveIntegerField(default=0)
    attack=models.PositiveIntegerField(default=0)
    deffence=models.PositiveIntegerField(default=0)
    picture=models.ImageField(default=None, blank=True, null=True)

    
    def __str__(self):
        return self.name