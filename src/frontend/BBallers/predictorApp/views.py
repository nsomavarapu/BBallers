from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, loader
import pickle, os, re, random
from django.templatetags.static import static
# Create your views here.
from django.http import HttpResponse

import goldsberry as gb
import pandas as pd
import requests
import json
from django.conf import settings

from django.views.decorators.csrf import ensure_csrf_cookie

open(os.path.join(settings.STATICFILES_DIRS[0], 'predictorApp/NBA-Visualization-gh-pages/logo/ATL_logo.svg'))

@ensure_csrf_cookie
def index(request):
	template = loader.get_template("predictorApp/index.html")
	return HttpResponse(template.render())
	
@ensure_csrf_cookie
def postTeams(request):
	print request
	if request.method == 'POST':
		text = request.POST.get('the_post')
		response_data = {}
		teams = getPlayoffPicture()
		response_data['result'] = (teams)
		response_data['text'] = text
		response_data['author'] = 'Mitch Donley'

		return HttpResponse(json.dumps(response_data), content_type="application/json")


def postResults(request):
	if request.method == 'POST':
		response_data = {}
		response_data['data'] = [ [], [], [], [] ]
		matchups = json.loads(request.POST['teams'])
		
		for j in range(0, 4):
			tempMatchup = []
			print matchups
			print "---------------------------------------"
			for i in range(0, len(matchups)):
				team1 = matchups[i][0]
				team2 = matchups[i][1]
				out = getPrediction(team1, team2)
				winner = out[0]
				games = out[1]
				team1Wins = 4 if winner == 'a' else games - 4
				team2Wins = 4 if winner == 'b' else games - 4
				teamWinAbbr = team1 if winner == 'a' else team2
				tempMatchup.append(teamWinAbbr)
				response_data['data'][j].append([team1Wins, team2Wins, {'a': team1, 'b': team2}])
			matchups = []
			for i in range(0, len(tempMatchup), 2):
				if len(tempMatchup) != 1:
					matchups.append([tempMatchup[i], tempMatchup[i+1]])
		print response_data['data']
		return HttpResponse(json.dumps(response_data), content_type="application/json")

def getPlayoffPicture():
	playoffsURL = 'http://stats.nba.com/stats/playoffpicture?LeagueID=00&SeasonID=22015'
	response = requests.get(playoffsURL)
	response.raise_for_status()
	eastPlayoffTeams = response.json()['resultSets'][0]['rowSet']
	eastPlayoffTable = pd.DataFrame(eastPlayoffTeams)
	eastTeams = eastPlayoffTable[[3, 6]]

	westPlayoffTeams = response.json()['resultSets'][1]['rowSet']
	westPlayoffTable = pd.DataFrame(westPlayoffTeams)
	westTeams = westPlayoffTable[[3, 6]]
	teams = pd.concat([eastTeams, westTeams])
	
	teamAbbrs = [None]*8

	infoURL = 'http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2015-16'
	response = requests.get(infoURL)
	response.raise_for_status()
	teamInfo = response.json()['resultSets'][0]['rowSet']
	info = pd.DataFrame(teamInfo)
	ordering = [0, 3, 2, 1, 4, 7, 6, 5]
	i = 0
	for index, teams in teams.iterrows():

		team1 = teams[3]
		team2 = teams[6]

		team1Abbr = info[info[7] == team1]
		team1Abbr = team1Abbr[10]
		team1Abbr = team1Abbr.values[0]

		team2Abbr = info[info[7] == team2]
		team2Abbr = team2Abbr[10]
		team2Abbr = team2Abbr.values[0]
		teamAbbr = [team1Abbr, team2Abbr]

		teamAbbrs[ordering[i]] = teamAbbr
		i = i + 1
	teamData = pd.DataFrame(teamAbbrs, columns = ["Team1", "Team2"])
	return teamData.to_json(orient = 'values')











player_dict = pickle.load(open(os.path.join(settings.STATICFILES_DIRS[0], 'predictorApp/production/players.p'), 'rb'))
player_team_dict = pickle.load(open(os.path.join(settings.STATICFILES_DIRS[0], 'predictorApp/production/players_team.p'), 'rb'))

weka_command = 'java -cp ' + os.path.join(settings.STATICFILES_DIRS[0], 'predictorApp/production/weka.jar') + ' weka.classifiers.functions.VotedPerceptron \
					 -T ' + os.path.join(settings.STATICFILES_DIRS[0], 'predictorApp/production/unclassified.arff') + '\
					 -l ' + os.path.join(settings.STATICFILES_DIRS[0], 'predictorApp/production/bballin.model')+  ' -p 0'

header = ['@relation player_diff-weka.filters.unsupervised.attribute.NumericToNominal-Rlast', '', '@attribute AST numeric', '@attribute BLK numeric', \
          '@attribute DREB numeric', '@attribute FG3A numeric', '@attribute FG3M numeric','@attribute FG3_PCT numeric', '@attribute FGA numeric', \
          '@attribute FGM numeric', '@attribute FG_PCT numeric', '@attribute FTA numeric', '@attribute FTM numeric', '@attribute FT_PCT numeric', \
          '@attribute OREB numeric', '@attribute PF numeric', '@attribute PLUS_MINUS numeric','@attribute PTS numeric', '@attribute REB numeric', \
          '@attribute STL numeric', '@attribute TOV numeric', '@attribute WL {-1,1}', '', '@data']

def getPrediction(team1, team2, player_arr1=None, player_arr2=None):
	# print player_dict
	# print settings.STATICFILES_DIRS
	# print player_team_dict

	player_arr1, player_arr2 = getPlayer(team1, team2) if (player_arr1==None and player_arr2==None) else (player_arr1, player_arr2)
	stats1 = []
	# print player_dict
	for player in player_arr1:
		if len(stats1) == 0:
			stats1 = player_dict[player]
		else:
			# print player
			stats1 = sum_arr(stats1, player_dict[player])

	stats2 = []
	for player in player_arr2:
		if len(stats2) == 0:
			stats2 = player_dict[player]
		else:
			stats2 = sum_arr(stats2, player_dict[player])

	
	
	total_stats = sub_arr(stats1, stats2) + [-1]
	str_ttl_stats = []
	for val in total_stats:
		str_ttl_stats.append(str(val))

	total_stats = str_ttl_stats

	arrf_header = '\n'.join(header)

	# print arrf_header
	f_w = open(os.path.join(settings.STATICFILES_DIRS[0], 'predictorApp/production/unclassified.arff'), 'wb')

	f_w.write(arrf_header + '\n')
	f_w.write(','.join(total_stats))
	f_w.write('\n')
	f_w.close()

	b = os.popen(weka_command)

	prediction = None
	for line in b:
		# print line
		split_line = line.split()

		if len(split_line) > 0:
			m = re.search(':',split_line[2])
			if m and split_line[3] == '+':
				prediction = (split_line[2].split(':')[1], split_line[4])
			elif m:
				prediction = (split_line[2].split(':')[1], split_line[3])
				

	team_prediction = None
	if prediction[0] == '1':
		# print "Team A wins with " + prediction[1] + " probability."
		team_prediction = ('a', random.randint(4,7))
	elif prediction[0] == '-1':
		# print "Team B wins with " + prediction[1] + " probability."
		team_prediction = ('b', random.randint(4,7))

	print team1, team2
	return team_prediction


# def getPlayerStats():

def sub_arr(arr1, arr2):
	# print arr1, arr2
	diff_arr = []
	for i in range(len(arr1)):
		diff_arr.append(float(arr1[i])-float(arr2[i]))

	return diff_arr	

def sum_arr(arr1, arr2):
	# print arr1, arr2
	sum_arr = []
	for i in range(len(arr1)):
		# print arr1[i], arr2[i]
		sum_arr.append(float(arr1[i])+float(arr2[i]))

	return sum_arr	

def getPlayer(team1, team2):
	# print team1, team2
	# print player_team_dict[team1], player_team_dict[team2]
	return player_team_dict[team1], player_team_dict[team2]