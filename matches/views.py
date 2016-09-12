from django.shortcuts import render, get_object_or_404
from .models import Match, Tip
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import TipForm
from leagues.models import League
from django.http import HttpResponseRedirect
from pip._vendor.requests.api import request
from django.contrib.auth.models import User
from django.utils import timezone

def list_matches(request, league):
    matches = Match.objects.filter(start_date__gt=datetime.now(), is_finished = False).order_by('start_date')[:8]
    matches_view = []
    for match in matches:
        tip = Tip.objects.filter(user = request.user, match = match, league = league)
        if tip.count() > 0:
            matches_view.append([match, tip.first()])
        else:
            matches_view.append([match, None])
    return {'matches_view': matches_view}

@login_required(login_url='/')
def maketips(request, league_id, match_id):
    league = get_object_or_404(League, id = league_id)
    match = get_object_or_404(Match, id = match_id)
    if timezone.make_aware(datetime.now(), timezone.get_default_timezone())  >= match.start_date:
        return HttpResponseRedirect('/leagues/my_league/' + league_id + '/')
    tip = Tip.objects.filter(user = request.user, match = match, league = league)
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            home_tip = form.cleaned_data['home_score_tip']
            away_tip = form.cleaned_data['away_score_tip']
            if tip.count() > 0:
                tip_to_save = tip.first()
            else:
                tip_to_save = Tip()
                tip_to_save.user = request.user
                tip_to_save.match = match
                tip_to_save.league = league
            tip_to_save.home_score_tip = home_tip
            tip_to_save.away_score_tip = away_tip
            tip_to_save.save()
            return HttpResponseRedirect('/leagues/my_league/' + league_id + '/')
        tip_form = form
    else:
        if tip.count() > 0:
            tip = tip.first()
            tip_form = TipForm(initial={'home_score_tip': tip.home_score_tip, 'away_score_tip': tip.away_score_tip})
        else:
            tip_form = TipForm(initial={'home_score_tip': 0, 'away_score_tip': 0})
        tip_form.fields['home_score_tip'].label = match.get_home_team_display
        tip_form.fields['away_score_tip'].label = match.get_away_team_display
    return render(request, 'matches/tips.html', {'tip_form': tip_form, 'match_id': match_id, 'league_id': league_id, 'league_name': league.league_name})
