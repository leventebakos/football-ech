from __future__ import unicode_literals
from django.db import models

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
		('NI', "Northern Ireland"),
		('PL', "Poland"),
		('PT', "Portugal"),
		('RI', "Republic of Ireland"),
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

	def __str__(self):
		return self.get_home_team_display() + "-" + self.get_away_team_display() + ": " + str(self.home_score) + "-" + str(self.away_score)
