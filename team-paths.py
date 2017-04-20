import json
import os
import sys

# '=' : 'Pass'
# '#' : 'Demo'
symbols = {
    'K': 'Kickoff',
    'I': 'Inbounds',
    'R': 'Rebound',
    '-': 'Steal',
    '+': 'Clear',
    '/': 'Yield',
    '*': 'Score',
    '!': 'Save',
    '?': 'Miss',
    '$': 'Timeout'
}

team_name = sys.argv[1]

file_in = open(sys.argv[2], 'r')

season = int(file_in.readline().strip())

season_teams_file_name = './Resources/season-%d-teams.json' % season
if not os.path.exists(season_teams_file_name):
    print('! ERROR: season teams file does not exist in json.')
    exit(0)

teams = None
with open(season_teams_file_name, 'r') as f_in:
    teams = json.loads(f_in.read().strip())

match = file_in.readline().strip().lower().replace(' ', '_')

blue_team = file_in.readline().strip().replace(' ', '_')
orange_team = file_in.readline().strip().replace(' ', '_')

blue_players = tuple(teams[blue_team])
orange_players = tuple(teams[orange_team])

symbols['A'] = blue_players[0]
symbols['B'] = blue_players[1]
symbols['C'] = blue_players[2]
symbols['X'] = orange_players[0]
symbols['Y'] = orange_players[1]
symbols['Z'] = orange_players[2]

file_out = open('./Paths/%s-%d.pdat' % (team_name, season), 'w')

if blue_team == team_name:
    path = ''
    for line in file_in:
        line = line.strip()
        if line == '' or line == '$':
            continue
        u, v, op, clock = line.split(' ')
        if op == '#':
            continue
        if (u == 'K' or u == 'I' or u == 'R') and (v == 'A' or v == 'B' or v == 'C'):
            path = '%s %s %s ' % (clock, symbols[u], symbols[v])
        elif op != '!' and (u == 'X' or u == 'Y' or u == 'Z') and (v == 'A' or v == 'B' or v == 'C'):
            path = '%s %s %s ' % (clock, symbols[op], symbols[v])
        elif (u == 'A' or u == 'B' or u == 'C') and (v == 'A' or v == 'B' or v == 'C'):
            path += '%s ' % (symbols[v])
        elif (u == 'A' or u == 'B' or u == 'C'):
            if path == '':
                continue
            path += '%s %s\n' % (symbols[op], clock)
            file_out.write(path)
            path = ''
        else:
            path = ''
        
        if clock == '0':
            path = ''
elif orange_team == team_name:
    path = ''
    for line in file_in:
        line = line.strip()
        if line == '' or line == '$':
            continue
        u, v, op, clock = line.split(' ')
        if op == '#':
            continue
        if (u == 'K' or u == 'I' or u == 'R') and (v == 'X' or v == 'Y' or v == 'Z'):
            path = '%s %s %s' % (clock, symbols[u], symbols[v])
        elif op != '!' and (u == 'A' or u == 'B' or u == 'C') and (v == 'X' or v == 'Y' or v == 'Z'):
            path = '%s %s %s' % (clock, symbols[op], symbols[v])
        elif (u == 'X' or u == 'Y' or u == 'Z') and (v == 'X' or v == 'Y' or v == 'Z'):
            path += '%s %s' % (symbols[u] , symbols[v])
        elif (u == 'X' or u == 'Y' or u == 'Z'):
            if path == '':
                continue
            path += '%s %s %s\n' % (symbols[u], symbols[op], clock)
            file_out.write(path)
            path = ''
        else:
            path = ''

        if clock == '0':
            path = ''

file_in.close()

file_in = open(sys.argv[3], 'r')

season = int(file_in.readline().strip())

season_teams_file_name = './Resources/season-%d-teams.json' % season
if not os.path.exists(season_teams_file_name):
    print('! ERROR: season teams file does not exist in json.')
    exit(0)

teams = None
with open(season_teams_file_name, 'r') as f_in:
    teams = json.loads(f_in.read().strip())

match = file_in.readline().strip().lower().replace(' ', '_')

blue_team = file_in.readline().strip().replace(' ', '_')
orange_team = file_in.readline().strip().replace(' ', '_')

blue_players = tuple(teams[blue_team])
orange_players = tuple(teams[orange_team])

symbols['A'] = blue_players[0]
symbols['B'] = blue_players[1]
symbols['C'] = blue_players[2]
symbols['X'] = orange_players[0]
symbols['Y'] = orange_players[1]
symbols['Z'] = orange_players[2]

if blue_team == team_name:
    path = ''
    for line in file_in:
        line = line.strip()
        if line == '' or line == '$':
            continue
        u, v, op, clock = line.split(' ')
        if op == '#':
            continue
        if (u == 'K' or u == 'I' or u == 'R') and (v == 'A' or v == 'B' or v == 'C'):
            path = '%s %s %s ' % (clock, symbols[u], symbols[v])
        elif op != '!' and (u == 'X' or u == 'Y' or u == 'Z') and (v == 'A' or v == 'B' or v == 'C'):
            path = '%s %s %s ' % (clock, symbols[op], symbols[v])
        elif (u == 'A' or u == 'B' or u == 'C') and (v == 'A' or v == 'B' or v == 'C'):
            path += '%s ' % (symbols[v])
        elif (u == 'A' or u == 'B' or u == 'C'):
            if path == '':
                continue
            path += '%s %s\n' % (symbols[op], clock)
            file_out.write(path)
            path = ''
        else:
            path = ''
        
        if clock == '0':
            path = ''
elif orange_team == team_name:
    path = ''
    for line in file_in:
        line = line.strip()
        if line == '' or line == '$':
            continue
        u, v, op, clock = line.split(' ')
        if op == '#':
            continue
        if (u == 'K' or u == 'I' or u == 'R') and (v == 'X' or v == 'Y' or v == 'Z'):
            path = '%s %s %s' % (clock, symbols[u], symbols[v])
        elif op != '!' and (u == 'A' or u == 'B' or u == 'C') and (v == 'X' or v == 'Y' or v == 'Z'):
            path = '%s %s %s' % (clock, symbols[op], symbols[v])
        elif (u == 'X' or u == 'Y' or u == 'Z') and (v == 'X' or v == 'Y' or v == 'Z'):
            path += '%s %s' % (symbols[u] , symbols[v])
        elif (u == 'X' or u == 'Y' or u == 'Z'):
            if path == '':
                continue
            path += '%s %s %s\n' % (symbols[u], symbols[op], clock)
            file_out.write(path)
            path = ''
        else:
            path = ''

        if clock == '0':
            path = ''

file_in.close()
file_out.close()