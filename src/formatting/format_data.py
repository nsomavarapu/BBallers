import csv, re, pickle
# from sklearn.neural_network import MLPClassifier

def gen_csv():
	f_r = open('AllTeams.csv', 'r')
	f_w = open('diff_data.csv', 'wb')
	csv_r = csv.reader(f_r)
	csv_w = csv.writer(f_w)

	header = csv_r.next()
	header_line = header[1:13] + header[17:22] + [header[23]] + [header[27]] + ['HOME'] 
	class_lbl = ['CLASS']
	total_header = header_line + class_lbl
	stats_dict = {}

	csv_w.writerow(total_header)


	for line in csv_r:
		home = False
		game_id = line[14]
		stats_line = line[1:13] + line[17:22] + [line[23]] + [line[27]] + [line[29]]

		s_group = re.search('@', line[15])
		if s_group is not None:
			home = True

		if game_id in stats_dict:
			w_l = 1 if stats_dict[game_id][-1] == 'W' else -1
			if home:
				stats_dict[game_id] = stats_line[:-1] + [1] + stats_dict[game_id][:-1] + [0] + [w_l]
			else:
				stats_dict[game_id] = stats_dict[game_id][:-1] + [1] + stats_line[:-1] + [0] + [w_l]
		else:
			stats_dict[game_id] = stats_line

	for key in stats_dict.keys():
		team1 = stats_dict[key][0:(40/2)]
		team2 = stats_dict[key][(40/2):-1]
		diff = []

		for i in range(len(team1)):
			diff.append(float(team1[i]) - float(team2[i]))

		csv_w.writerow(diff + [stats_dict[key][-1]])
	f_r.close()
	f_w.close()

def get_player_csv(file_list, data_directory):

	game_dict = {}
	player_dict = {}

	game_ctr = 0
	player_ctr = 0

	game_index = 14
	player_index = 33
	drop_indices = []

	for f in file_list:
		f_r = open(data_directory + f, 'r')
		csv_r = csv.reader(f_r)

		header_line = csv_r.next()
		header = header_line[1:13] + header_line[17:21] + [header_line[22]] + [header_line[24]] + [header_line[25]] + [header_line[27]]

		for line in csv_r:

			stats_line = line[1:13] + line[17:21] + [line[22]] + [line[24]] + [line[25]]
			player_ident = line[player_index]

			if line[35] != '':
				game_id = (line[game_index].lstrip('0'), line[35])
				
				if game_id not in game_dict.keys():
					game_dict[game_id] = [line[27], line[33]]
				else:
					game_dict[game_id].append(line[33])

			if player_ident not in player_dict.keys():
				player_dict[player_ident] = stats_line
			else:
				player_dict[player_ident] = sum_arr(player_dict[player_ident], stats_line)
		player_ctr += 1
		f_r.close()

	new_dict = {}
	for k,v in game_dict.iteritems():
		if len(game_dict[k]) >= 5:
			new_dict[k] = v

	for k,v in new_dict.iteritems():
		wl_list = [new_dict[k][0]]
		curr_stats_list = []
		for player in new_dict[k]:
			if player in player_dict.keys():
				if len(curr_stats_list) == 0:
					curr_stats_list = player_dict[player]
				else:
					sum_arr(curr_stats_list, player_dict[player])
		new_dict[k] = curr_stats_list + wl_list

	end_dict = {}
	for k,v in new_dict.iteritems():
		if k[0] not in end_dict.keys():
			end_dict[k[0]] = [v]
		else:
			end_dict[k[0]].append(v)

	for k,v in end_dict.iteritems():
		class_val = end_dict[k][0][-1]
		combined_stats = sub_arr(end_dict[k][0][:-1], end_dict[k][1][:-1])
		if class_val == 'W':
			class_val = 1
		elif class_val == 'L':
			class_val = -1

		end_dict[k] = combined_stats + [class_val]

	f_w = open('player_diff.csv', 'wb')
	csv_w = csv.writer(f_w)
	csv_w.writerow(header)
	# print header
	for k,v in end_dict.iteritems():
		csv_w.writerow(v)
		# print v 
		# print "---------------------------------"

	f_w.close()


	pickle.dump(player_dict, open('players.p', 'wb'))
		

	# for k in player_dict.keys():
	# 	new_arr = []
	# 	for val in player_dict[k]:
	# 		if type(val) is not str:
	# 			new_arr.append(val/float(player_ctr))
	# 	player_dict[k] = new_arr

	# for k,v in player_dict.iteritems():
	# 	print k, v
	# 	print "---------------------------------"


def sub_arr(arr1, arr2):
	# print arr1, arr2
	sum_arr = []
	for i in range(len(arr1)):
		sum_arr.append(float(arr1[i])-float(arr2[i]))

	return sum_arr
		

def sum_arr(arr1, arr2):
	# print arr1, arr2
	sum_arr = []
	for i in range(len(arr1)):
		sum_arr.append(float(arr1[i])+float(arr2[i]))

	return sum_arr

def getTPdict(file_list, data_directory):

	player_team_dict = {}
	for f in file_list:
		f_r = open(data_directory + f, 'r')
		csv_r = csv.reader(f_r)
		csv_r.next()

		for line in csv_r:
			team_iden = line[35]
			# print line[33]
			if team_iden not in player_team_dict.keys():
				player_team_dict[team_iden] = [line[33]]
			elif line[33] not in player_team_dict[team_iden]:
				player_team_dict[team_iden].append(line[33])

		f_r.close()

	# print player_team_dict
	pickle.dump(player_team_dict, open('players_team.p', 'wb'))


if __name__ == '__main__':
	file_list = ['AllGames.csv']
	data_directory = '../../data/'
	get_player_csv(file_list, data_directory)
	getTPdict(file_list, data_directory)

	# gen_csv()
	# print "works"