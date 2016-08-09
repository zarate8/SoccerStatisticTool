from lxml import html
from bs4 import BeautifulSoup
import requests
import argparse
import json

def parseDate(date):
    #TODO: Ensure date is in the correct format
    darr = date.split('-')
    return darr[2] + darr[0] + darr[1]

def parse(date):
    date = parseDate(date)
    # TODO: Make the league interchangable
    url = 'http://espndeportes.espn.com/futbol/fixtures/_/fecha/' + date + '/liga/mex.1'
    print 'fetching data from...'
    print url

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")

    lines = soup.find_all("tr", {"class":["odd","even"]})


    matches = []
    for line in lines:
        '''
        print line.contents[0].find_all("a", {"class":"team-name"})[0].find_all("span")[0].text + ' ' + \
            line.contents[0].find_all("span", {"class":"record"})[0].find_all("a")[0].text + ' ' + \
            line.contents[1].find_all("a", {"class":"team-name"})[0].find_all("span")[0].text             
            '''  
        home = line.contents[0].find_all("a", {"class":"team-name"})[0].find_all("span")[0].text
        away = line.contents[1].find_all("a", {"class":"team-name"})[0].find_all("span")[0].text
        score = line.contents[0].find_all("span", {"class":"record"})[0].find_all("a")[0].text.split(' - ')
        
        if len(score) > 1:
            gameObj = {'home' : 
                       {'name' : home,'score': score[0]},\
                           'away' :{'name' : away,'score': score[1]}}
            #print(json.dumps(gameObj))
            matches.append(gameObj)
    return matches
                
parser = argparse.ArgumentParser()
parser.add_argument("date", help="Date of the page you want parsed, is the following format mm/dd/yyyy",
                    type=str)
args = parser.parse_args()

print args.date
parse(args.date)
