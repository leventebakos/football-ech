from django import forms

class LeagueForm(forms.Form):
    league_name = forms.CharField(label = "Group name", max_length = 30)
    max_size = forms.IntegerField(label = "Maximum participants", min_value = 0, max_value = 9999)
    points_for_exact_guess = forms.IntegerField(label = "Points for exact guess", min_value = 0, max_value = 100)
    points_for_goal_difference = forms.IntegerField(label = "Points for goal difference", min_value = 0, max_value = 100)
    points_for_outcome = forms.IntegerField(label = "Points for outcome", min_value = 0, max_value = 100)
    points_for_number_of_goals = forms.IntegerField(label = "Points for number of goals", min_value = 0, max_value = 100)
    points_for_exact_home_goals = forms.IntegerField(label = "Points for exact home goals", min_value = 0, max_value = 100)
    points_for_exact_away_goals = forms.IntegerField(label = "Points for exact away goals", min_value = 0, max_value = 100)