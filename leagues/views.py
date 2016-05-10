from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LeagueForm
from .models import League, LeagueParticipants
from matches.models import Match, Tip
from django.http import HttpResponseRedirect
from pip._vendor.requests.api import request
from django.contrib.auth.models import User

@login_required(login_url='/')
def create_league(request):
    if request.method == 'POST':
        league_form = LeagueForm(request.POST)
        if league_form.is_valid():
            league_to_save = league_form_to_league_converter(league_form)
            league_to_save.save()
            league_participant_to_save = league_participant_from_league_form(league_to_save, request)
            league_participant_to_save.save()
            return HttpResponseRedirect('/leagues/my_leagues/')
        league_form = league_form
    else:
        league_form = LeagueForm()
    return render(request, 'leagues/create_league.html', {'league_form': league_form})

@login_required(login_url='/')
def get_leagues(request):
    leagues_from_participants = LeagueParticipants.objects.values_list('league', flat=True)
    leagues = League.objects.filter(pk__in=leagues_from_participants).all()
    return render(request, 'leagues/my_leagues.html', {'leagues': leagues})

@login_required(login_url='/')
def list_available_leagues(request):
    leagues_to_return = []
    leagues = League.objects.all()
    for league in leagues:
        max_participants_in_league = league.max_size
        current_participants_in_league = LeagueParticipants.objects.filter(league = league).count()
        if current_participants_in_league < max_participants_in_league and LeagueParticipants.objects.filter(user = request.user, league = league).count() == 0:
            leagues_to_return.append(league)
    return render(request, 'leagues/list_available_leagues.html', {'leagues': leagues_to_return})

@login_required(login_url='/')
def join_league(request, id):
    league = get_object_or_404(League, id = id)
    league_participant = LeagueParticipants.objects.filter(user = request.user, league = league)
    if league_participant.count() == 0:
        league_participant_to_save = league_participant_from_league_form(league, request)
        league_participant_to_save.save()
    return HttpResponseRedirect('/leagues/my_leagues/')

@login_required(login_url='/')
def league_details(request, id):
    league = get_object_or_404(League, id = id)
    if LeagueParticipants.objects.filter(user = request.user, league = league).count() == 0:
        return HttpResponseRedirect('/leagues/my_leagues/')
    standings = get_standings(request, league)
    return render(request, 'leagues/league_details.html', {'standings': standings})
    
def league_form_to_league_converter(league_form):
    result = League()
    result.league_name = league_form.cleaned_data['league_name']
    result.max_size = league_form.cleaned_data['max_size']
    result.points_for_exact_guess = league_form.cleaned_data['points_for_exact_guess']
    result.points_for_goal_difference = league_form.cleaned_data['points_for_goal_difference']
    result.points_for_outcome = league_form.cleaned_data['points_for_outcome']
    result.points_for_number_of_goals = league_form.cleaned_data['points_for_number_of_goals']
    result.points_for_exact_home_goals = league_form.cleaned_data['points_for_exact_home_goals']
    result.points_for_exact_away_goals = league_form.cleaned_data['points_for_exact_away_goals']
    return result
    
def league_participant_from_league_form(league_to_save, request):
    result = LeagueParticipants()
    result.user = request.user
    result.league = league_to_save
    return result

def get_standings(request, league):
    league_participant_ids = LeagueParticipants.objects.values_list('user', flat=True).filter(league = league)
    users = User.objects.filter(id__in = league_participant_ids).all()
    users_and_scores = []
    for user in users:
        users_and_scores.append((user, calculate_scores(user, league)))
    return users_and_scores

def calculate_scores(user, league):
    result = 0
    finished_matches = Match.objects.filter(is_finished = True)
    for match in finished_matches:
        tip = Tip.objects.filter(league = league, match = match, user = user)
        if tip.count() == 0:
            continue
        else:
            tip = tip.first()
            home_score_tip = tip.home_score_tip
            away_score_tip = tip.away_score_tip
            actual_home_score = match.home_score
            actual_away_score = match.away_score
            if is_exact_guess(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
                result += league.points_for_exact_guess
            if correct_goal_difference(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
                result += league.points_for_goal_difference
            if correct_outcome(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
                result += league.points_for_outcome
            if correct_number_of_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
                result += league.points_for_number_of_goals
            if correct_home_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
                result += league.points_for_exact_home_goals
            if correct_away_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
                result += league.points_for_exact_away_goals
    return result

def is_exact_guess(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
    return home_score_tip == actual_home_score and away_score_tip == actual_away_score

def correct_goal_difference(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
    return home_score_tip - away_score_tip == actual_home_score - actual_away_score

def correct_outcome(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
    result = False
    if  actual_home_score == actual_away_score and home_score_tip == away_score_tip:
        result = True
    elif actual_home_score > actual_away_score and home_score_tip > away_score_tip:
        result = True
    elif actual_home_score < actual_away_score and home_score_tip < away_score_tip:
        result = True
    return result
        
def correct_number_of_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
    return home_score_tip + away_score_tip == actual_home_score + actual_away_score

def correct_home_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
    return home_score_tip == actual_home_score

def correct_away_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score):
    return away_score_tip == actual_away_score


    