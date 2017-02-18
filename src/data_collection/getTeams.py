import goldsberry as gb
import pandas as pd
import numpy as np


westTeams = [['Golden State Warriors', 1610612744], ['San Antonio Spurs', 1610612759], ['Oklahoma City Thunder', 1610612760], ['Los Angeles Clippers', 1610612746], ['Memphis Grizzlies', 1610612763], ['Portland Trailblazers' , 1610612757],  ['Dallas Mavericks', 1610612742], ['Houston Rockets', 1610612745]]
eastTeams = [['Cleveland Cavaliers', 1610612739], ['Toronto Raptors', 1610612761], ['Atlanta Hawks', 1610612737], ['Boston Celtics', 1610612738], ['Miami Heat', 1610612748], ['Charlotte Hornets', 1610612766], ['Detroit Pistons', 1610612765], ['Indiana Pacers', 1610612754]]
gameids = gb.GameIDs()
players = gb.PlayerList()
gameids2015 = pd.DataFrame(gameids.game_list())
gameids2015.to_csv('AllTeams.csv')
players2015 = pd.DataFrame(players.players())



for i in range(0, 4):
	team1WestName = westTeams[i][0]
	team1WestID = westTeams[i][1]
	team1WestPlayers = players2015[players2015['TEAM_ID'] == team1WestID]
	team1WestLog = gameids2015[gameids2015['TEAM_ID'] == team1WestID]


	team1WestPlayerID = team1WestPlayers['PERSON_ID']
	team1WestPlayerGameLog = []
	for personID in team1WestPlayerID:
		team1WestPlayerGameLog.append(pd.DataFrame(gb.player.game_logs(personID).logs()))

	team1WestPlayerGameLog = pd.concat(team1WestPlayerGameLog)
	team1WestPlayerGameLog = pd.merge(team1WestPlayerGameLog, team1WestPlayers, right_on = ['PERSON_ID'], left_on = ['Player_ID'], how = 'outer')
	'''print team1WestPlayerGameLog'''
	

	team2WestName = westTeams[len(westTeams) - 1 - i][0]
	team2WestID = westTeams[len(westTeams) - 1 - i][1]
	team2WestPlayers = players2015[players2015['TEAM_ID'] == team2WestID]
	team2WestLog = gameids2015[gameids2015['TEAM_ID'] == team2WestID]
	team2WestPlayerID = team2WestPlayers['PERSON_ID']
	team2WestPlayerGameLog = []
	for personID in team2WestPlayerID:
		team2WestPlayerGameLog.append(pd.DataFrame(gb.player.game_logs(personID).logs()))

	team2WestPlayerGameLog = pd.concat(team2WestPlayerGameLog)
	team2WestPlayerGameLog = pd.merge(team2WestPlayerGameLog, team2WestPlayers, right_on = ['PERSON_ID'], left_on = ['Player_ID'], how = 'outer')


	team1EastName = eastTeams[i][0]
	team1EastID = eastTeams[i][1]
	team1EastLog = gameids2015[gameids2015['TEAM_ID'] == team1EastID]
	team1EastPlayers = players2015[players2015['TEAM_ID'] == team1EastID]
	team1EastPlayerID = team1EastPlayers['PERSON_ID']
	team1EastPlayerGameLog = []
	for personID in team1EastPlayerID:
		team1EastPlayerGameLog.append(pd.DataFrame(gb.player.game_logs(personID).logs()))

	team1EastPlayerGameLog = pd.concat(team1EastPlayerGameLog)
	team1EastPlayerGameLog = pd.merge(team1EastPlayerGameLog, team1EastPlayers, right_on = ['PERSON_ID'], left_on = ['Player_ID'], how = 'outer')


	team2EastName = eastTeams[len(westTeams) - 1 - i][0]
	team2EastID = eastTeams[len(westTeams) - 1 - i][1]
	team2EastLog = gameids2015[gameids2015['TEAM_ID'] == team2EastID]
	team2EastPlayers = players2015[players2015['TEAM_ID'] == team2EastID]
	team2EastPlayerID = team2EastPlayers['PERSON_ID']
	team2EastPlayerGameLog = []
	for personID in team2EastPlayerID:
		team2EastPlayerGameLog.append(pd.DataFrame(gb.player.game_logs(personID).logs()))

	team2EastPlayerGameLog = pd.concat(team2EastPlayerGameLog) 
	team2EastPlayerGameLog = pd.merge(team2EastPlayerGameLog, team2EastPlayers, right_on = ['PERSON_ID'], left_on = ['Player_ID'], how = 'outer')


	westgame = pd.concat([team1WestLog, team2WestLog])
	eastgame = pd.concat([team1EastLog, team2EastLog])
	westPlayers = pd.concat([team1WestPlayerGameLog, team2WestPlayerGameLog])
	eastPlayers = pd.concat([team1EastPlayerGameLog, team2EastPlayerGameLog])

	westgame.to_csv('WestGame' + str(i) + '.csv')
	westPlayers.to_csv('WestPlayers' + str(i) + '.csv')
	eastgame.to_csv('EastGame' + str(i) + '.csv')
	eastPlayers.to_csv('EastPlayers' + str(i) + '.csv')

