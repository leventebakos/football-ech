from django.shortcuts import render, get_object_or_404
from .models import Match, Tip
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import TipForm
from django.http import HttpResponseRedirect

@login_required(login_url='/')
def list_matches(request):
    matches = Match.objects.filter(start_date__gt=datetime.now())
    matches_view = []
    for match in matches:
        tip = Tip.objects.filter(user = request.user, match = match)
        if tip.count() > 0:
            matches_view.append([match, tip.first()])
        else:
            matches_view.append([match, None])
    context = {'matches_view': matches_view}
    return render(request, 'matches/list_matches.html', context)

@login_required(login_url='/')
def maketips(request, id):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        match = get_object_or_404(Match, id = id)
        tip = Tip.objects.filter(user = request.user, match = match)
        if tip.count() > 0:
            tip = tip.first()
            tip_form = TipForm(match.home_team, match.away_team, tip.home_score_tip, tip.away_score_tip)
        else:
            tip_form = TipForm(match.home_team, match.away_team)

    return render(request, 'matches/tips.html', {'tip_form': tip_form})
    