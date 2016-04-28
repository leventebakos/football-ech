from django import forms

class TipForm(forms.Form):
    home_score_tip = forms.IntegerField(label = "Home score tip", min_value = 0)
    away_score_tip = forms.IntegerField(label = "Away score tip", min_value = 0)
    