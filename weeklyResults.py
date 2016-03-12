import sys
import xml.etree.ElementTree as ET
#tree = ET.parse('resultados.xml')
tree = ET.parse('output.xml')
root = tree.getroot()

jornada = 'jornada9'
week = root.findall(jornada)

#User picks the week they want to view
# else display first week

# Team abreviations
Teams = {
'V':'Veracruz',
'At':'Atlas',
'S':'Santos',
'Pa':'Pachuca',
'CA':'Cruz Azul',
'Pu':'Puebla',
'Tig':'Tigres',
'Pm':'Pumas UNAM',
'L':'Leon',
'Q':'Queretaro',
'Mor':'Morelia',
'Mon':'Monterrey',
'J':'Jaguares',
'Tij':'Tijuana',
'Tol':'Toluca',
'D':'Dorados',
'Ch':'Chivas',
'Am':'America'}

def viewResults():
    for w in week:
        for game in w.findall('game'):
            g = ''
            for team in game.findall('team'):
                goals = team.get('goals')
                name = team.get('name')
                if g == '':
                    g += str(name) + ' ' + str(goals) + ' vs '
                else:
                    g += str(name) + ' ' + str(goals)
                    expected = game.find('expected').text
                    print g + ' Expected ->\t' + expected

def viewTeam(team_name):
    for w in week:
        for game in w.findall('game'):
            for team in game.findall('team'):
                name = team.get('name')
                if name == team_name:
                    return team

def updateTeamGoals(team_name, goals):
    for w in week:
        for game in w.iter('game'):
            for team in game.iter('team'):
                name = team.get('name')
                if name == team_name:                    
                    team.set('goals', goals)

def writeToFile():
    tree.write('output.xml')

def getTeamList():
    list = ''
    for team in Teams.keys():
        list += team + ' -> ' + Teams[team] + '\n'
    return list

alen = len(sys.argv)
if alen == 1:
    message = 'To modify the results add flag -m followed by weed to modify: python resultadosParser.py -m 10\n'
    message += 'To view the whole week\'s results specify the week number: python resultadosParser.py 10'
    print message
    
if alen == 2:
    jornada = 'jornada' + sys.argv[1]
    week = root.findall(jornada)
    viewResults()

if alen == 3:
    if sys.argv[1] == '-m': # If user wants to modify the xml
        jornada = 'jornada' + sys.argv[2]
        week = root.findall(jornada)
        
        team_list = getTeamList()

        while True:
            team = raw_input(team_list + '\n To stop: STOP\n'+ 'What team would you like to modify? ')
            
            if team == 'STOP':
                break

            goals = raw_input('How many Goals:  ')
            if team in Teams:
                team_name = Teams[team]
                updateTeamGoals(team_name, goals)
                print (team + ' has been modified ')        
                t = viewTeam(team_name)
                print team + ' ' + t.get('goals')

        writeToFile()

#elif alen == 2:
    
    
    