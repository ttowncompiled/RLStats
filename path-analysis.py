import json
import os
from pprint import pprint
from scipy.stats import kendalltau
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

true_ranks = [
    'FlipSid3_Tactics',
    'Mock-It_Aces',
    'Northern_Gaming',
    'Take_3',
    'NRG',
    'Precision_Z',
    'Genesis',
    'Orbit'
]

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

print('Rankings according to average team path length:')
pprint(team_path_length)
print('Kendall-Tau constant:')
print(kendalltau(true_ranks, map(lambda x: x[1], team_path_length)))

print('Rankings according to average team flow rate:')
pprint(team_flow_rate)
print('Kendall-Tau constant:')
print(kendalltau(true_ranks, map(lambda x: x[1], team_flow_rate)))
