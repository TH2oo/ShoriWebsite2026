from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username


class Team(models.Model):
    name = models.CharField(max_length=60, unique=True)
    logo_name = models.CharField(
        max_length=60,
        help_text="Nom du fichier sans extension (ex: Shori → Teams=Shori.png)",
    )
    color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        help_text="Couleur primaire en hexadécimal (ex: #971C22)",
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Match(models.Model):
    datetime = models.DateTimeField()
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='home_matches',
    )
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='away_matches',
    )
    location = models.CharField(max_length=120)

    class Meta:
        ordering = ['datetime']
        verbose_name_plural = 'matches'

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} — {self.datetime:%d/%m/%Y %H:%M}"

