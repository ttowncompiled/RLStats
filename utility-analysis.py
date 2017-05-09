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

team_flow = {}
for t, players in teams.iteritems():
    team_path_file = './Paths/%s-s_%d.pdat' % (t, season)
    if not os.path.exists(team_path_file):
        print('! ERROR: team path file does not exist (%s).' % t)
        exit(0)
    paths = 0
    player_flow = {}
    for p in players:
        player_flow[p] = 0
    with open(team_path_file, 'r') as f:
        for line in f:
            line = line.strip()
            nodes = line.split(' ')[1:-1]
            N = {}
            for n in nodes:
                N[n] = True
            for n in N.keys():
                if n in player_flow:
                    player_flow[n] += 1
            paths += 1
    for p in players:
        player_flow[p] = round((player_flow[p] * 1.0) / paths, 3)
    team_flow[t] = player_flow

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

ranks = []
for t, player_flow in team_flow.iteritems():
    f = 0
    for p, flow in player_flow.iteritems():
        f += flow
    f = round((f * 1.0) / 3, 3)
    ranks.append((f, t))

ranks.sort()

print('Rankings according to average individual flow centrality:')
pprint(ranks)
print('Kendall-Tau constant:')
print(kendalltau(true_ranks, map(lambda x: x[1], ranks)))

team_flow = {}
for t, players in teams.iteritems():
    team_path_file = './Paths/%s-s_%d.pdat' % (t, season)
    if not os.path.exists(team_path_file):
        print('! ERROR: team path file does not exist (%s).' % t)
        exit(0)
    paths = 0
    player_flow = {}
    for p in players:
        player_flow[p] = 0
    with open(team_path_file, 'r') as f:
        for line in f:
            line = line.strip()
            nodes = line.split(' ')[1:-1]
            if len(nodes) > 3:
                nodes = nodes[-3:]
            N = {}
            for n in nodes:
                N[n] = True
            for n in N.keys():
                if n in player_flow:
                    player_flow[n] += 1
            paths += 1
    for p in players:
        player_flow[p] = round((player_flow[p] * 1.0) / paths, 3)
    team_flow[t] = player_flow

ranks = []
for t, player_flow in team_flow.iteritems():
    f = 0
    for p, flow in player_flow.iteritems():
        f += flow
    f = round((f * 1.0) / 3, 3)
    ranks.append((f, t))

ranks.sort()
ranks.reverse()

print('Rankings according to average restricted individual flow centrality:')
pprint(ranks)
print('Kendall-Tau constant:')
print(kendalltau(true_ranks, map(lambda x: x[1], ranks)))

team_flow = {}
for t, players in teams.iteritems():
    team_path_file = './Paths/%s-s_%d.pdat' % (t, season)
    if not os.path.exists(team_path_file):
        print('! ERROR: team path file does not exist (%s).' % t)
        exit(0)
    player_flow = {}
    for p in players:
        player_flow[p] = (0, 0, 0)
    with open(team_path_file, 'r') as f:
        for line in f:
            line = line.strip()
            nodes = line.split(' ')[1:-1]
            if len(nodes) > 3:
                nodes = nodes[-3:]
            N = {}
            for n in nodes:
                N[n] = True
            for n in N.keys():
                if n in player_flow:
                    flow = player_flow[n]
                    if nodes[-1] == 'Score':
                        flow = (flow[0] + 1, flow[1], 0)
                    else:
                        flow = (flow[0], flow[1] + 1, 0)
                    player_flow[n] = flow
    for p in players:
        flow = player_flow[p]
        flow = (flow[0], flow[1], round((flow[0] * 1.0) / (flow[0] + flow[1]), 3))
        player_flow[p] = flow
    team_flow[t] = player_flow

ranks = []
for t, player_flow in team_flow.iteritems():
    f = 0
    for p, flow in player_flow.iteritems():
        f += flow[2]
    f = round((f * 1.0) / 3, 3)
    ranks.append((f, t))

ranks.sort()

print('Rankings according to average player utility:')
pprint(ranks)
print('Kendall-Tau constant:')
print(kendalltau(true_ranks, map(lambda x: x[1], ranks)))
