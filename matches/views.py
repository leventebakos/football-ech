from django.shortcuts import render
from .models import Match, Tip
from datetime import datetime
from django.contrib.auth.decorators import login_required

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