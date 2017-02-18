import pickle, os

player_dict = pickle.load(open('players.p', 'rb'))
weka_command = 'java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -T unclassified.arff -l bballin.model -p 0'
header = ['@relation player_diff-weka.filters.unsupervised.attribute.NumericToNominal-Rlast', '', '@attribute AST numeric', '@attribute BLK numeric', \
          '@attribute DREB numeric', '@attribute FG3A numeric', '@attribute FG3M numeric','@attribute FG3_PCT numeric', '@attribute FGA numeric', \
          '@attribute FGM numeric', '@attribute FG_PCT numeric', '@attribute FTA numeric', '@attribute FTM numeric', '@attribute FT_PCT numeric', \
          '@attribute OREB numeric', '@attribute PF numeric', '@attribute PLUS_MINUS numeric','@attribute PTS numeric', '@attribute REB numeric', \
          '@attribute STL numeric', '@attribute TOV numeric', '@attribute WL {-1,1}', '', '@data']

def getPrediction(player_arr1, player_arr2):
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

	
	
	total_stats = sub_arr(stats1, stats2) + [0]
	str_ttl_stats = []
	for val in total_stats:
		str_ttl_stats.append(str(val))

	total_stats = str_ttl_stats

	arrf_header = '\n'.join(header)

	# print arrf_header

	f_w = open('unclassified.arff', 'wb')

	f_w.write(arrf_header + '\n')
	f_w.write(','.join(total_stats))
	f_w.close()

	os.system(weka_command)


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

if __name__ == '__main__':
	getPrediction(['stephen_curry', 'klay_thompson', 'draymond_green', 'andre_iguodala', 'andrew_bogut'],['demarcus_cousins', 'rajon_rondo', 'seth_curry', 'rudy_gay', 'omri_casspi'])