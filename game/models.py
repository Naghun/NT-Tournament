from django.db import models

# Create your models here.
class Card(models.Model):

    RACE = (
        ('Human', 'Human'),
        ('Fantasy', 'Fantasy'),
        ('Creature', 'Creature'),
        ('Alien', 'Alien'),
    )

    TIER_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )


    id=models.IntegerField(blank=True, primary_key=True)
    name=models.CharField(max_length=100)
    race=models.CharField(max_length=50, choices=RACE, default=None)
    tier = models.IntegerField(choices=TIER_CHOICES, default=1, null=True, blank=True)
    overall=models.PositiveIntegerField(default=0)
    speed=models.IntegerField(default=0, null=True, blank=True)
    health=models.PositiveIntegerField(default=0)
    attack=models.PositiveIntegerField(default=0)
    deffence=models.PositiveIntegerField(default=0)
    crit=models.IntegerField(default=0)
    fatique=models.IntegerField(default=0)
    picture=models.ImageField(default=None, blank=True, null=True, upload_to='images/')
    wins=models.IntegerField(default=0, blank=True, null=True)

    
    def __str__(self):
        return self.name
    

class InitialCards(models.Model):
    id=models.IntegerField(blank=True, primary_key=True)
    name=models.CharField(max_length=100)
    overall=models.PositiveIntegerField(default=0)
    speed=models.IntegerField(default=0, null=True, blank=True)
    health=models.PositiveIntegerField(default=0)
    attack=models.PositiveIntegerField(default=0)
    deffence=models.PositiveIntegerField(default=0)
    wins=models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    tournament=models.PositiveIntegerField(default=1)
    year=models.PositiveIntegerField(default=1)

    def increase_year(self):
        if self.tournament == 366:
            self.tournament=1
            self.year +=1
        else:
            self.tournament+=1
        self.save()

    def __str__(self):
        return f"Year: {self.year}, Tournament: {self.tournament}"
    
class Winners(models.Model):
    tournament_number= models.BigIntegerField(default=0)
    tournament_year=models.IntegerField(default=0)
    winner=models.CharField(max_length=250)

    def __str__(self):
        return self.winner
