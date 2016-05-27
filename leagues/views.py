from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LeagueForm
from .models import League, LeagueParticipants
from matches.models import Match, Tip
from matches.views import list_matches
from django.http import HttpResponseRedirect
from pip._vendor.requests.api import request
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum
import string, random

@login_required(login_url='/')
def create_league(request):
    if request.method == 'POST':
        league_form = LeagueForm(request.POST)
        if league_form.is_valid():
            league_to_save = league_form_to_league_converter(league_form, request)
            league_to_save.save()
            league_participant_to_save = league_participant_from_league_form(league_to_save, request)
            league_participant_to_save.save()
            return HttpResponseRedirect('/leagues/my_leagues/')
        league_form = league_form
    else:
        league_form = LeagueForm()
    return render(request, 'leagues/create_league.html', {'league_form': league_form})

@login_required(login_url='/')
def get_my_leagues(request):
    leagues_from_participants = LeagueParticipants.objects.values_list('league', flat=True).filter(user = request.user)
    leagues = League.objects.filter(pk__in=leagues_from_participants).all()
    return render(request, 'leagues/my_leagues.html', {'leagues': leagues})

@login_required(login_url='/')
def list_available_leagues(request):
    leagues_to_return = []
    users_private_leagues_to_return = []
    leagues = League.objects.all()
    for league in leagues:
        if league.is_private == False:
            max_participants_in_league = league.max_size
            current_participants_in_league = LeagueParticipants.objects.filter(league = league).count()
            if current_participants_in_league < max_participants_in_league and LeagueParticipants.objects.filter(user = request.user, league = league).count() == 0:
                leagues_to_return.append([league, max_participants_in_league - current_participants_in_league])
        elif league.is_private == True and league.creator == request.user:
            users_private_leagues_to_return.append(league)
    return render(request, 'leagues/list_available_leagues.html', {'leagues': leagues_to_return, 'users_private_leagues_to_return': users_private_leagues_to_return})

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
    scoring_conditions = get_league_scoring_conditions(league);
    standings = get_standings(league)
    matches = list_matches(request, league)
    group_A_matches = get_group_matches("A", league, request)
    group_B_matches = get_group_matches("B", league, request)
    group_C_matches = get_group_matches("C", league, request)
    group_D_matches = get_group_matches("D", league, request)
    group_E_matches = get_group_matches("E", league, request)
    group_F_matches = get_group_matches("F", league, request)
    group_A_header = get_group_headers("A")
    group_B_header = get_group_headers("B")
    group_C_header = get_group_headers("C")
    group_D_header = get_group_headers("D")
    group_E_header = get_group_headers("E")
    group_F_header = get_group_headers("F")
    return render(request, 'leagues/league_details.html', {'standings': standings, 'matches_view': matches['matches_view'], 'league_id': id, 'scoring_conditions': scoring_conditions, 'league_name': league.league_name, 'group_A_matches': group_A_matches, 'group_A_header': group_A_header, 'group_B_matches': group_B_matches, 'group_B_header': group_B_header, 'group_C_matches': group_C_matches, 'group_C_header': group_C_header, 'group_D_matches': group_D_matches, 'group_D_header': group_D_header, 'group_E_matches': group_E_matches, 'group_E_header': group_E_header, 'group_F_matches': group_F_matches, 'group_F_header': group_F_header})

def get_group_matches(group_id, league, request):
    matches = Match.objects.filter(group = group_id).order_by('start_date')
    users_from_participants = LeagueParticipants.objects.values_list('user', flat=True).filter(league = league)
    users = User.objects.filter(pk__in=users_from_participants).all()
    result = []
    to_append = ["Results"]
    for match in matches:
        if match.is_finished:
            to_append.append(str(match.home_score) + "-" + str(match.away_score))
        else:
            to_append.append("No results yet")
    result.append(to_append)
    for user in users:
        to_append = [user.first_name + " " + user.last_name]
        for match in matches:
            if match.is_finished or timezone.make_aware(datetime.now(), timezone.get_default_timezone())  >= match.start_date:
                tip = Tip.objects.filter(league = league, match = match, user = user)
                if tip.count() > 0:
                    tip = tip.first()
                    if match.is_finished:
                        to_append.append('<table class="table table-striped table-bordered"><tr><td>' + str(tip.home_score_tip) + '-' + str(tip.away_score_tip) + '</td><td>' + str(tip.score) + ' points</td></tr></table>')
                    else:
                        to_append.append(str(tip.home_score_tip) + "-" + str(tip.away_score_tip))
                else:
                    to_append.append("No tip")
            else:
                if user == request.user:
                    tip = Tip.objects.filter(league = league, match = match, user = user)
                    link_text = "Tip"
                    if tip.count() > 0:
                        tip = tip.first()
                        link_text = str(tip.home_score_tip) + "-" + str(tip.away_score_tip) 
                    to_append.append('<a href="/leagues/' + str(league.id) + '/tip/' + str(match.id) + '/">' + link_text + '</a>')
                    
                else:
                    to_append.append("Game not started yet")
        result.append(to_append)
    return result

def get_group_headers(group_id):
    return Match.objects.filter(group = group_id).order_by('start_date')
 
def league_form_to_league_converter(league_form, request):
    result = League()
    result.league_name = league_form.cleaned_data['league_name']
    result.max_size = league_form.cleaned_data['max_size']
    result.points_for_exact_guess = league_form.cleaned_data['points_for_exact_guess']
    result.points_for_goal_difference = league_form.cleaned_data['points_for_goal_difference']
    result.points_for_outcome = league_form.cleaned_data['points_for_outcome']
    result.points_for_number_of_goals = league_form.cleaned_data['points_for_number_of_goals']
    result.points_for_exact_home_goals = league_form.cleaned_data['points_for_exact_home_goals']
    result.points_for_exact_away_goals = league_form.cleaned_data['points_for_exact_away_goals']
    result.is_private = league_form.cleaned_data['is_private']
    if result.is_private:
        result.league_secret_key = generate_league_secret_key()
    result.creator = request.user
    return result
    
def generate_league_secret_key():    
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(10))
    
def league_participant_from_league_form(league_to_save, request):
    result = LeagueParticipants()
    result.user = request.user
    result.league = league_to_save
    return result

def get_standings(league):
    league_participant_ids = LeagueParticipants.objects.values_list('user', flat=True).filter(league = league)
    users = User.objects.filter(id__in = league_participant_ids).all()
    users_and_scores = []
    for user in users:
        users_and_scores.append((user, calculate_scores(user, league)))
    return users_and_scores

def calculate_scores(user, league):
    correct_tips = init_correct_tips(league)
    result = 0
    finished_matches = Match.objects.filter(is_finished = True)
    for match in finished_matches:
        tip = Tip.objects.filter(league = league, match = match, user = user)
        if tip.count() != 0:
            tip = tip.first()
            if tip.is_score_calculated == False:
                update_tip_with_score(tip)
    all_user_tips = Tip.objects.filter(league = league, user = user)
    if all_user_tips.count() > 0:
        result = all_user_tips.aggregate(Sum('score'))
        result = int(result['score__sum'])
        update_correct_tips(correct_tips, league, all_user_tips)
    return (result, correct_tips)

def update_tip_with_score(tip):
    score = 0
    scoring_field = ""
    home_score_tip = tip.home_score_tip
    away_score_tip = tip.away_score_tip
    actual_home_score = tip.match.home_score
    actual_away_score = tip.match.away_score
    if is_exact_guess(home_score_tip, away_score_tip, actual_home_score, actual_away_score) and tip.league.points_for_exact_guess > score:
        score = tip.league.points_for_exact_guess
        scoring_field = "exact_guess"
    if correct_goal_difference(home_score_tip, away_score_tip, actual_home_score, actual_away_score) and tip.league.points_for_goal_difference > score:
        score = tip.league.points_for_goal_difference
        scoring_field = "goal_difference"
    if correct_outcome(home_score_tip, away_score_tip, actual_home_score, actual_away_score) and tip.league.points_for_outcome > score:
        score = tip.league.points_for_outcome
        scoring_field = "outcome"
    if correct_number_of_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score) and tip.league.points_for_number_of_goals > score:
        score = tip.league.points_for_number_of_goals
        scoring_field = "number_of_goals"
    if correct_home_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score) and tip.league.points_for_exact_home_goals > score:
        score = tip.league.points_for_exact_home_goals
        scoring_field = "home_goals"
    if correct_away_goals(home_score_tip, away_score_tip, actual_home_score, actual_away_score) and tip.league.points_for_exact_away_goals > score:
        score = tip.league.points_for_exact_away_goals
        scoring_field = "away_goals"
    tip.score = score
    tip.scoring_field = scoring_field
    tip.is_score_calculated = True
    tip.save()

def init_correct_tips(league):
    result = {}
    if league.points_for_exact_guess != 0:
        result["exact_guess"] = 0
    if league.points_for_goal_difference != 0:
        result["goal_difference"] = 0
    if league.points_for_outcome != 0:
        result["outcome"] = 0
    if league.points_for_number_of_goals != 0:
        result["number_of_goals"] = 0
    if league.points_for_exact_home_goals != 0:
        result["home_goals"] = 0
    if league.points_for_exact_away_goals != 0:
        result["away_goals"] = 0
    return result

def update_correct_tips(correct_tips, league, all_user_tips):
    if league.points_for_exact_guess != 0:
        correct_tips["exact_guess"] = all_user_tips.filter(scoring_field = "exact_guess").count()
    if league.points_for_goal_difference != 0:
        correct_tips["goal_difference"] = all_user_tips.filter(scoring_field = "goal_difference").count()
    if league.points_for_outcome != 0:
        correct_tips["outcome"] = all_user_tips.filter(scoring_field = "outcome").count()
    if league.points_for_number_of_goals != 0:
        correct_tips["number_of_goals"] = all_user_tips.filter(scoring_field = "number_of_goals").count()
    if league.points_for_exact_home_goals != 0:
        correct_tips["home_goals"] = all_user_tips.filter(scoring_field = "home_goals").count()
    if league.points_for_exact_away_goals != 0:
        correct_tips["away_goals"] = all_user_tips.filter(scoring_field = "away_goals").count()

def get_league_scoring_conditions(league):
    result = []
    if league.points_for_exact_guess != 0:
        result.append("Exact guess")
    if league.points_for_goal_difference != 0:
        result.append("Correct outcome with goal difference")
    if league.points_for_outcome != 0:
        result.append("Correct outcome")
    if league.points_for_number_of_goals != 0:
        result.append("Correct number of goals")
    if league.points_for_exact_home_goals != 0:
        result.append("Correct number of home goals")
    if league.points_for_exact_away_goals != 0:
        result.append("Correct number of away goals")
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


    