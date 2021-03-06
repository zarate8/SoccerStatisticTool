import argparse
from espnParser import parse, parseDate
import os;
from database.databaseCalls import getTeamId
from database.databaseCalls import insertMatch
import database.databaseCalls
import json

db = database.databaseCalls
parser = argparse.ArgumentParser()
parser.add_argument("date", help="Date of games you want to add to database.",
                    type=str)
args = parser.parse_args()
#print args.date

os.chdir(os.getcwd() + '/database') # Must change current working direcory to where the config file is located


def saveMatches():
    print '\n\n\n\n'
    matches = parse(args.date)
    for o in matches:
        homeId =  getTeamId(o['home']['name'])
        homeScore = o['home']['score']
        awayId =  getTeamId(o['away']['name'])
        awayScore = o['away']['score']
        winner = matchWinner(homeId, homeScore, awayId, awayScore)

        date = formatDate(args.date)
        insertMatch(homeId, homeScore, awayId, awayScore, winner, date)


def updateMatches(date):
    print '\n\n\n\n'
    matches = parse(args.date)
    for o in matches:
        homeId =  getTeamId(o['home']['name'])
        homeScore = o['home']['score']
        awayId =  getTeamId(o['away']['name'])
        awayScore = o['away']['score']
        winner = matchWinner(homeId, homeScore, awayId, awayScore)
        date = formatDate(args.date)
        matchId = db.getMatchId(homeId, awayId, date)

        db.updateMatchScore(matchId, homeScore, awayScore, winner)
        recordSingleMatchRacha(matchId, homeId, homeScore, awayId, awayScore, date)

        
def matchWinner(homeId, homeScore, awayId, awayScore):
    if homeScore > awayScore:
        return homeId
    elif homeScore < awayScore:
        return awayId
    else:# A tie is represented by 0
        return 0
        

def recordSingleMatchRacha(matchId, homeId, homeScore, awayId, awayScore, date):
    results = db.getResults()
    homeResult = compareMatchResults(homeId, awayId, results)
    awayResult = compareMatchResults(awayId, homeId, results)
    
    db.insertRachaEntry(matchId, homeId, homeResult, date)
    db.insertRachaEntry(matchId, awayId, awayResult, date)
    

# Records racha for all games in database
def recordRacha(date):
    matches = db.getMatches(date)

    results = db.getResults()
    for match in matches:
        date = match[6]
        # parameters matchId, currentTeam, win/lose/tie, date
        db.insertRachaEntry(match[0], match[1], compareMatchResults(match[2], match[4], results), date)
        db.insertRachaEntry(match[0], match[3], compareMatchResults(match[4], match[2], results), date)


def recordPredictions(fileName, date):
    matches = parsePredictionFile(fileName)
    
    for match in matches:
        homeId = getTeamId(match[0])
        awayId = getTeamId(match[1])
        prediction = db.getPredictionId(match[2])

        print 'prediction ' + match[2]
        print 'home ' + str(homeId)
        print 'away ' + str(awayId)
        print 'predict ' + str(prediction)

        matchId = db.getMatchId(homeId, awayId, date)

        if matchId is not None:
            db.insertPrediction(matchId, prediction)
        else:
            print 'Error: No match is recorded for the date provided.'

def parsePredictionFile(fileName):
    array = []
    with open(fileName) as f:

        for line in f:
            print line
            c = line.decode('utf8')
            cont = c.split(',')
            array.append((cont[0], cont[2], cont[3].rstrip()))

    return array

# Determine winner of the game
def compareMatchResults(teamScore, oponentScore, resultOptions):
    # Team wins
    if teamScore > oponentScore:
        return resultOptions[0][0]
    # Team loses
    elif teamScore < oponentScore:
        return resultOptions[1][0]
    # Match is a draw
    else:
        return resultOptions[2][0]

# Format date for sql query    
def formatDate(date):
    d = date.split('-')
    return  d[2] + d[0] + d[1]
    


#recordRacha(formatDate(args.date))

# Save matches to database
#saveMatches()

#print parsePredictionFile('../matches.txt')
#print recordPredictions('../matches.txt', formatDate(args.date))

#print db.getPredictionId('P')

# Update matches after matches have been added with initial scores of 0
#updateMatches(formatDate(args.date))
   


    
