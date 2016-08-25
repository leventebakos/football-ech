from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from leagues.models import League
from django.db.models.signals import post_save
from django.dispatch import receiver

class Match(models.Model):
	COUNTRY_CHOICES = (
		('PS', "Paris Saint-Germain"),
		('AR', "Arsenal"),
		('BA', "Basel"),
		('LU', "Ludogorec Razgrad"),
		('BN', "Benfica"),
		('NA', "Napoli"),
		('DK', "Dinamo Kijev"),
		('BS', "Besiktas"),
		('BC', "Barcelona"),
		('MC', "Manchester City"),
		('BM', "Borussia Monchengladbach"),
		('CE', "Celtic"),
		('BY', "Bayern Munchen"),
		('AM', "Atletico Madrid"),
		('PE', "PSV Eindhoven"),
		('RS', "FK Rosztov"),
		('CM', "CSZKA Moszkva"),
		('BL', "Bayer Leverkusen"),
		('TO', "Tottenham"),
		('MO', "Monaco"),
		('RM', "Real Madrid"),
		('BD', "Borussia Dortmund"),
		('SC', "Sporting CP"),
		('LW', "Legia Warszawa"),
		('LC', "Leicester City"),
		('PP', "Porto"),
		('BR', "FC Bruges"),
		('KO', "Kobenhavn"),
		('JU', "Juventus"),
		('SV', "Sevilla"),
		('LY', "Lyon"),
		('DZ', "Dinamo Zagreb")
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
	score = models.IntegerField(default = 0)
	scoring_field = models.CharField(max_length = 256, blank = True)
	is_score_calculated = models.BooleanField(default = False)
	
	def __str__(self):
		return self.user.username + " - " + self.league.league_name + ": " + self.match.home_team + " - " + self.match.away_team + ": " + str(self.home_score_tip) + " - " + str(self.away_score_tip)
