from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class League(models.Model):
    league_name = models.CharField(max_length = 256)
    max_size = models.IntegerField()
    points_for_exact_guess = models.IntegerField()
    points_for_goal_difference = models.IntegerField()
    points_for_outcome = models.IntegerField()
    points_for_number_of_goals = models.IntegerField()
    points_for_exact_home_goals = models.IntegerField()
    points_for_exact_away_goals = models.IntegerField()
    is_private = models.BooleanField(default = False)
    league_secret_key = models.CharField(max_length = 256, blank = True, null = True)
    creator = models.ForeignKey(User, models.CASCADE, blank = True, null = True)
    
    def __str__(self):
        return self.league_name
    
class LeagueParticipants(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    league = models.ForeignKey(League, models.CASCADE)
    
    def __str__(self):
        return self.league.league_name + " - " + self.user.username