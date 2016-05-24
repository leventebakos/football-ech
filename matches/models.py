from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from leagues.models import League

class Match(models.Model):
	COUNTRY_CHOICES = (
		('AL', "Albania"),
		('AT', "Austria"),
		('BE', "Belgium"),
		('HR', "Croatia"),
		('CZ', "Czech"),
		('EN', "England"),
		('FR', "France"),
		('DE', "Germany"),
		('HU', "Hungary"),
		('IS', "Iceland"),
		('IT', "Italy"),
		('NI', "N. Ireland"),
		('PL', "Poland"),
		('PT', "Portugal"),
		('RI', "R. of Ireland"),
		('RO', "Romania"),
		('RU', "Russia"),
		('SK', "Slovakia"),
		('SP', "Spain"),
		('SE', "Sweden"),
		('SW', "Switzerland"),
		('TK', "Turkey"),
		('UK', "Ukraine"),
		('WA', "Wales"),
	)
	home_team = models.CharField(max_length = 2, choices = COUNTRY_CHOICES)
	away_team = models.CharField(max_length = 2, choices = COUNTRY_CHOICES)
	home_score = models.IntegerField(default = 0)
	away_score = models.IntegerField(default = 0)
	start_date = models.DateTimeField()
	is_finished = models.BooleanField(default = False)
	group = models.CharField(max_length = 20, null = True)

	def __str__(self):
		return self.get_home_team_display() + "-" + self.get_away_team_display() + ": " + str(self.home_score) + "-" + str(self.away_score) + "___" + str(self.start_date) + " group: " + str(self.group)

class Tip(models.Model):
	user = models.ForeignKey(User, models.CASCADE)
	league = models.ForeignKey(League, models.CASCADE, null = True)
	match = models.ForeignKey(Match, models.CASCADE)
	home_score_tip = models.IntegerField()
	away_score_tip = models.IntegerField()
	
	def __str__(self):
		return self.user.username + " - " + self.league.league_name + ": " + self.match.home_team + " - " + self.match.away_team + ": " + str(self.home_score_tip) + " - " + str(self.away_score_tip)
	
