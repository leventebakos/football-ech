from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class League(models.Model):
    league_name = models.CharField(max_length = 30)
    max_size = models.IntegerField()
    points_for_exact_guess = models.IntegerField()
    points_for_goal_difference = models.IntegerField()
    points_for_outcome = models.IntegerField()
    points_for_number_of_goals = models.IntegerField()
    points_for_exact_home_goals = models.IntegerField()
    points_for_exact_away_goals = models.IntegerField()
    
    def __str__(self):
        return self.league_name
    
class LeagueParticipants(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    league = models.ForeignKey(League, models.CASCADE)
    
    def __str__(self):
        return self.league.league_name + " - " + self.user.username