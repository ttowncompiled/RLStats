import json
import os
from pprint import pprint
import sys

season = int(sys.argv[1])

season_teams_file_name = './Resources/season-%d-teams.json' % season
if not os.path.exists(season_teams_file_name):
    print('! ERROR: season teams file does not exist in json.')
    exit(0)

teams = None
with open(season_teams_file_name, 'r') as f_in:
    teams = json.loads(f_in.read().strip())

for t, players in teams.iteritems():
    team_path_file = './Paths/%s-s_%d.pdat' % (t, season)
    if not os.path.exists(team_path_file):
        print('! ERROR: team path file does not exist (%s).' % t)
        exit(0)
    paths = 0
    player_part = {}
    for p in players:
        player_part[p] = 0
    with open(team_path_file, 'r') as f:
        for line in f:
            line = line.strip()
            nodes = line.split(' ')[1:-1]
            N = {}
            for n in nodes:
              N[n] = True
            for n in N.keys():
                if n in player_part:
                    player_part[n] += 1
            paths += 1
    print(player_part)
