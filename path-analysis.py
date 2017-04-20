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

teams = teams.keys()

team_path_length = []
team_flow_rate = []

for t in teams:
    team_path_file = './Paths/%s-s_%d.pdat' % (t, season)
    if not os.path.exists(team_path_file):
        print('! ERROR: team path file does not exist (%s).' % t)
        exit(0)
    paths = 0
    lengths = 0
    flow = 0
    with open(team_path_file, 'r') as f:
        for line in f:
            line = line.strip()
            parts = line.split(' ')
            start, stop = int(parts[0]), int(parts[-1])
            nodes = parts[0:-1]
            paths += 1
            lengths += len(nodes) - 2 - 1
            flow += (abs(start - stop) * 1.0) / len(nodes)
    avg_path_len = (lengths * 1.0) / paths
    avg_flow_rate = (flow * 1.0) / paths

    team_path_length.append((avg_path_len, t))
    team_flow_rate.append((avg_flow_rate, t))

team_path_length.sort()
team_flow_rate.sort()

pprint(team_path_length)
team_path_length.reverse()
pprint(team_path_length)

pprint(team_flow_rate)
team_flow_rate.reverse()
pprint(team_flow_rate)