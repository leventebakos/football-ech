from django import forms

class TipForm(forms.Form):
    home_score_tip = forms.IntegerField(min_value = 0)
    away_score_tip = forms.IntegerField(min_value = 0)
    
    def __init__(self, home_label, away_label, home_score_tip = "", away_score_tip = ""):
        super(forms.Form, self).__init__()
        self.fields['home_score_tip'].label = home_label
        self.fields['away_score_tip'].label = away_label
        self.fields['home_score_tip'].initial = home_score_tip
        self.fields['away_score_tip'].initial = away_score_tip
    