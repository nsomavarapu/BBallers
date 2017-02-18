import pickle, os, re, random

player_dict = pickle.load(open('players.p', 'rb'))
player_team_dict = pickle.load(open('players_team.p', 'rb'))
weka_command = 'java -cp weka.jar weka.classifiers.functions.VotedPerceptron -T unclassified.arff -l bballin.model -p 0'
header = ['@relation player_diff-weka.filters.unsupervised.attribute.NumericToNominal-Rlast', '', '@attribute AST numeric', '@attribute BLK numeric', \
          '@attribute DREB numeric', '@attribute FG3A numeric', '@attribute FG3M numeric','@attribute FG3_PCT numeric', '@attribute FGA numeric', \
          '@attribute FGM numeric', '@attribute FG_PCT numeric', '@attribute FTA numeric', '@attribute FTM numeric', '@attribute FT_PCT numeric', \
          '@attribute OREB numeric', '@attribute PF numeric', '@attribute PLUS_MINUS numeric','@attribute PTS numeric', '@attribute REB numeric', \
          '@attribute STL numeric', '@attribute TOV numeric', '@attribute WL {-1,1}', '', '@data']

def getPrediction(team1, team2, player_arr1=None, player_arr2=None):
	# print player_dict
	player_arr1, player_arr2 = getPlayer(team1, team2) if (player_arr1==None and player_arr2==None) else (player_arr1, player_arr2)
	stats1 = []
	for player in player_arr1:
		if len(stats1) == 0:
			stats1 = player_dict[player]
		else:
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

	f_w = open('unclassified.arff', 'wb')

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

	print team_prediction


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
		sum_arr.append(float(arr1[i])+float(arr2[i]))

	return sum_arr	

def getPlayer(team1, team2):
	return player_team_dict[team1], player_team_dict[team2]

if __name__ == '__main__':
	# team_arrs = getPlayer('GSW', 'SAS')
	arr_a = ['kevin_durant', 'russell_westbrook', 'steven_adams', 'serge_ibaka', 'andre_roberson']#, 'enes_kanter', 'dion_waiters', 'randy_foye', 'kyle_singler', 'cameron_payne']
	# arr_a = ['demarcus_cousins', 'rajon_rondo', 'rudy_gay', 'seth_curry', 'omri_casspi']
	# arr_a = ['tony_parker', 'tim_duncan', 'lamarcus_aldridge', 'kawhi_leonard', 'emanuel_ginobili']
	arr_b = ['stephen_curry', 'klay_thompson', 'draymond_green', 'harrison_barnes', 'andrew_bogut']#, 'andre_iguodala', 'festus_ezeli', 'marreese_speights', 'shaun_livingston', 'leandro_barbosa']
	# player_arr1=arr_a, player_arr2=arr_b
	getPrediction('','', player_arr1=arr_a, player_arr2=arr_b)