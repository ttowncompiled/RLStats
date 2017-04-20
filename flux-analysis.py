import json
import networkx as nx
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

team_stats = {}

for t, players in teams.iteritems():
    team_path_file = './Graphs/%s-s_%d.gexf' % (t, season)
    if not os.path.exists(team_path_file):
        print('! ERROR: team path file does not exist (%s).' % t)
        exit(0)
    g = nx.read_gexf(team_path_file)
    player_stats = {}
    for p in players:
        scores = g.get_edge_data(p, 'Score')['weight']
        saves = g.get_edge_data(p, 'Save')['weight']
        misses = g.get_edge_data(p, 'Miss')['weight']
        shots = scores + saves + misses
        stats = {
            'scores': scores,
            'saves': saves,
            'misses': misses,
            'shots': shots,
            '%': round((scores * 1.0) / shots, 3)
        }
        player_stats[p] = stats
    team_stats[t] = player_stats

pprint(team_stats)

ranks = []

for t, player_stats in team_stats.iteritems():
    s = 0
    for p, stats in player_stats.iteritems():
        s += stats['%']
    s = (s * 1.0) / 3
    ranks.append((round(s, 3), t))

ranks.sort()
ranks.reverse()

pprint(ranks)

nodes = ['Steal', 'Clear', 'Score', 'Save', 'Miss', 'Yield', 'Timeout']
ranks = []

for t, player_stats in team_stats.iteritems():
    team_path_file = './Graphs/%s-s_%d.gexf' % (t, season)
    if not os.path.exists(team_path_file):
        print('! ERROR: team path file does not exist (%s).' % t)
        exit(0)
    g = nx.read_gexf(team_path_file)
    players = teams[t]
    flux = 0
    for i in players:
        w = 0
        for n in nodes + players:
            if i == n:
                continue
            w += g.get_edge_data(i, n)['weight']
        for j in players:
            if i == j:
                continue
            w_ij = g.get_edge_data(i, j)['weight']
            p_ij = (w_ij * 1.0) / w
            x_i = player_stats[i]['%']
            x_j = player_stats[j]['%']
            f = p_ij * (x_j - x_i)
            flux += f
    ranks.append((round(flux, 3), t))

ranks.sort()
ranks.reverse()

pprint(ranks)