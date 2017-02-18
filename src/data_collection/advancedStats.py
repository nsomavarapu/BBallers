import goldsberry as gb
import pandas as pd
import numpy as np
import requests
import os


westTeams = [['GoldenStateWarriors', 1610612744], ['SanAntonioSpurs', 1610612759], ['OklahomaCityThunder', 1610612760], ['LosAngelesClippers', 1610612746], ['MemphisGrizzlies', 1610612763], ['PortlandTrailblazers' , 1610612757],  ['DallasMavericks', 1610612742], ['HoustonRockets', 1610612745]]
eastTeams = [['ClevelandCavaliers', 1610612739], ['TorontoRaptors', 1610612761], ['AtlantaHawks', 1610612737], ['BostonCeltics', 1610612738], ['MiamiHeat', 1610612748], ['CharlotteHornets', 1610612766], ['DetroitPistons', 1610612765], ['IndianaPacers', 1610612754]]
gameids = gb.GameIDs()
players = gb.PlayerList()
gameids2015 = pd.DataFrame(gameids.game_list())
players2015 = pd.DataFrame(players.players())



def getPlayersOnTeam(teamID):
	teamPlayers = players2015[players2015['TEAM_ID'] == teamID]['PERSON_ID']
	return teamPlayers

# PLAYER STATS

def getPlayerShotDashboard(playerID, season = 2015-16, OpponentTeamID = 0):
	players = gb.player._Player2.shot_dashboard(playerID)
	overall = players.overall()
	return pd.DataFrame(overall)

def getPlayerReboundDashboard(playerID, season = 2015-16, OpponentTeamID = 0):
	players = gb.player._Player2.rebound_dashboard(playerID)
	rebounds = players.overall()
	return pd.DataFrame(rebounds)

def getPlayerPassingDashboard(playerID, season = 2015-16, OpponentTeamID = 0):
	players = gb.player._Player2.passing_dashboard(playerID)
	passing = players.passes_made()
	passes_made = pd.DataFrame(passing)
	passesOut = players.passes_received()
	passes_received = pd.DataFrame(passesOut)
	passes = pd.concat([passes_made, passes_received])
	return pd.DataFrame(passes)

def getPlayerDefenseDashboard(playerID, season = 2015-16, OpponentTeamID = 0):
	players = gb.player._Player2.defense_dashboard(playerID)
	defense = players.defending_shot()
	return pd.DataFrame(defense)

# GAME STATS

def getBoxScoreAdv(gameID):
	boxscoreAdv = gb.game._Game2.boxscore_advanced(gameID)
	return pd.DataFrame(boxscoreAdv.player_stats())

def getBoxScoreFourFactor(gameID):
	fourFactor = gb.game._Game2.boxscore_fourfactors(gameID)
	return pd.DataFrame(fourFactor.player_stats())

def getBoxScoreMisc(gameID):
	misc = gb.game._Game2.boxscore_miscellaneous(gameID)
	return pd.DataFrame(misc.player_stats())

def getBoxScoreScoring(gameID):
	scoring = gb.game._Game2.boxscore_scoring(gameID)
	return pd.DataFrame(scoring.player_stats())

def getBoxScoreSummary(gameID):
	summary = gb.game._Game2.boxscore_summary(gameID)
	return pd.concat([pd.DataFrame(summary.game_summary()), pd.DataFrame(summary.other_stats()), pd.DataFrame(summary.season_series())])

def getBoxScoreTracking(gameID):
	tracking = gb.game._Game2.boxscore_tracking(gameID)
	return pd.DataFrame(tracking.player_stats())

def getBoxScoreTraditional(gameID):
	traditional = gb.game._Game2.boxscore_traditional(gameID)
	return pd.DataFrame(traditional.player_stats())

def getBoxScoreUsage(gameID):
	usage = gb.game._Game2.boxscore_usage(gameID)
	return pd.DataFrame(usage.player_stats())

# TEAM STATS

def getTeamDefense(teamID):
	defense = gb.team._Team2.defense_dashboard(teamID)
	return pd.DataFrame(defense.defending_shot())

def getTeamGameLogs(teamID):
	GameLogs = gb.team._Team2.game_logs(teamID)
	return pd.DataFrame(GameLogs.logs())

def getTeamLineups(teamID):
	Lineups = gb.team._Team2.lineups(teamID)
	return pd.concat([pd.DataFrame(Lineups.overall()), pd.DataFrame(Lineups.lineups())])

def getTeamPassing(teamID):
	Passing = gb.team._Team2.passing_dashboard(teamID)
	return pd.concat([pd.DataFrame(Passing.passes_made()), pd.DataFrame(Passing.passes_received())])

def getTeamOn_Off_Court(teamID):
	On_Off_Court = gb.team._Team2.on_off_court(teamID)
	return pd.concat([pd.DataFrame(On_Off_Court.overall()), pd.DataFrame(On_Off_Court.on_court()), pd.DataFrame(On_Off_Court.off_court())])

def getTeamRebound(teamID):
	Rebound = gb.team._Team2.rebound_dashboard(teamID)
	return pd.concat([pd.DataFrame(Rebound.shot_type()), pd.DataFrame(Rebound.contesting_rebounders()), pd.DataFrame(Rebound.rebound_distance())])


def getTeamShot(teamID):
	Shot = gb.team._Team2.shot_dashboard(teamID)
	return pd.concat([pd.DataFrame(Shot.general()), pd.DataFrame(Shot.shot_clock()), pd.DataFrame(Shot.dribble()), pd.DataFrame(Shot.closest_defender()), pd.DataFrame(Shot.closest_defender_10ft()), pd.DataFrame(Shot.touch_time())])

def getTeamShotSplit(teamID):
	ShotSplit = gb.team._Team2.shooting_splits(teamID)
	return pd.concat([pd.DataFrame(ShotSplit.overall()), pd.DataFrame(ShotSplit.shot_5ft()), pd.DataFrame(ShotSplit.shot_8ft()), pd.DataFrame(ShotSplit.shot_area()), pd.DataFrame(ShotSplit.assisted_shot()), pd.DataFrame(ShotSplit.shot_type())])

def getTeamSplits(teamID):
	Splits = gb.team._Team2.splits(teamID)
	return pd.concat([pd.DataFrame(Splits.overall()), pd.DataFrame(Splits.location()), pd.DataFrame(Splits.wins_losses()), pd.DataFrame(Splits.month()), pd.DataFrame(Splits.pre_post_allstar()), pd.DataFrame(Splits.days_rest())])

def getTeamClutch():
	Clutch = gb.league._League2.team_stats_clutch()
	return pd.DataFrame(Clutch.clutch_stats())

if __name__ == '__main__':
	
	#print team
	# playerID = 201939
	# playerShotDash = getPlayerShotDashboard(playerID)
	# playerReboundDash = getPlayerReboundDashboard(playerID)
	# playerPassDash = getPlayerPassingDashboard(playerID)
	# playerDefenseDash = getPlayerDefenseDashboard(playerID)

	# playerShotDash.to_csv('Player_Shot_Dashboard' + str(playerID) + '.csv')
	# playerReboundDash.to_csv('Player_Rebound_Dashboard' + str(playerID) + '.csv')
	# playerPassDash.to_csv('Player_Passing_Dashboard' + str(playerID) + '.csv')
	# playerDefenseDash.to_csv('Player_Defense_Dashboard' + str(playerID) + '.csv')
	newpath = '/Users/MitchDonley/Documents/College/College_Homework/ECE_4813_Madasetti/BBallers/data/'
	#getTeamClutch().to_csv(os.path.join(newpath, 'TeamClutch.csv'))
	for team in westTeams:
		newpath = newpath + str(team[0]) + "_games"
		if not os.path.exists(newpath):
			print "Path doesnt exist"
			os.makedirs(newpath)
		gameIDs = gameids2015[gameids2015['TEAM_ID'] == team[1]]
		newgameIDs = gameIDs[['GAME_ID']]
		newgameIDs = newgameIDs[0:2]
		#getTeamDefense(team[1]).to_csv(os.path.join(newpath, 'TeamDefense.csv'))
		getTeamLineups(team[1]).to_csv(os.path.join(newpath, 'TeamLineups.csv'))
		getTeamPassing(team[1]).to_csv(os.path.join(newpath, 'TeamPassing.csv'))
		getTeamOn_Off_Court(team[1]).to_csv(os.path.join(newpath, 'TeamOnOffCourt.csv'))
		#getTeamRebound(team[1]).to_csv(os.path.join(newpath, 'TeamRebounding.csv'))
		#getTeamShot(team[1]).to_csv(os.path.join(newpath, 'TeamShot.csv'))
		getTeamShotSplit(team[1]).to_csv(os.path.join(newpath, 'TeamShotSplits.csv'))
		getTeamSplits(team[1]).to_csv(os.path.join(newpath, 'TeamSplits.csv'))

		for index, game in newgameIDs.iterrows():
			game = game['GAME_ID']
			getBoxScoreAdv(game).to_csv(os.path.join(newpath, 'Advanced_boxScore_' + str(game) + '.csv'))
			getBoxScoreFourFactor(game).to_csv(os.path.join(newpath, 'FourFactor_boxScore_' + str(game) + '.csv'))
			getBoxScoreMisc(game).to_csv(os.path.join(newpath, 'Misc_boxScore_' + str(game) + '.csv'))
			#getBoxScoreScoring(game).to_csv('Team_' + str(team) + '_Scoring_boxScore_' + str(game) + '.csv')
			getBoxScoreSummary(game).to_csv(os.path.join(newpath, 'Summary_boxScore_' + str(game) + '.csv'))
			getBoxScoreTracking(game).to_csv(os.path.join(newpath, 'Tracking_boxScore_' + str(game) + '.csv'))
			getBoxScoreTraditional(game).to_csv(os.path.join(newpath, 'Traditional_boxScore_' + str(game) + '.csv'))
			getBoxScoreUsage(game).to_csv(os.path.join(newpath, 'Usage_boxScore_' + str(game) + '.csv'))

		newpath = '/Users/MitchDonley/Documents/College/College_Homework/ECE_4813_Madasetti/BBallers/data/'

	for team in eastTeams:
		newpath = newpath + str(team[0]) + "_games"
		print newpath
		if not os.path.exists(newpath):
			print "Path doesnt exist"
			os.makedirs(newpath)
		print team[0]
		gameIDs = gameids2015[gameids2015['TEAM_ID'] == team[1]]
		newgameIDs = gameIDs[['GAME_ID']]
		newgameIDs = newgameIDs[0:2]
		for index, game in newgameIDs.iterrows():
			game = game['GAME_ID']
			getBoxScoreAdv(game).to_csv(os.path.join(newpath, 'Advanced_boxScore_' + str(game) + '.csv'))
			getBoxScoreFourFactor(game).to_csv(os.path.join(newpath, 'FourFactor_boxScore_' + str(game) + '.csv'))
			getBoxScoreMisc(game).to_csv(os.path.join(newpath, 'Misc_boxScore_' + str(game) + '.csv'))
			#getBoxScoreScoring(game).to_csv('Team_' + str(team) + '_Scoring_boxScore_' + str(game) + '.csv')
			getBoxScoreSummary(game).to_csv(os.path.join(newpath, 'Summary_boxScore_' + str(game) + '.csv'))
			getBoxScoreTracking(game).to_csv(os.path.join(newpath, 'Tracking_boxScore_' + str(game) + '.csv'))
			getBoxScoreTraditional(game).to_csv(os.path.join(newpath, 'Traditional_boxScore_' + str(game) + '.csv'))
			getBoxScoreUsage(game).to_csv(os.path.join(newpath, 'Usage_boxScore_' + str(game) + '.csv'))
		newpath = '/Users/MitchDonley/Documents/College/College_Homework/ECE_4813_Madasetti/BBallers/data/'
	