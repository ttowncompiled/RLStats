import json
import networkx as nx
import os
import sys

team_name = sys.argv[1]
season = int(sys.argv[2])

season_teams_file_name = './Resources/season-%d-teams.json' % season
if not os.path.exists(season_teams_file_name):
    print('! ERROR: season teams file does not exist in json.')
    exit(0)

teams = None
with open(season_teams_file_name, 'r') as f_in:
    teams = json.loads(f_in.read().strip())

players = tuple(teams[team_name])
possessions = ['Kickoff', 'Inbounds', 'Rebound', 'Steal', 'Clear']
outcomes = ['Steal', 'Clear', 'Score', 'Save', 'Miss', 'Yield', 'Timeout']

graph_1_path = sys.argv[3]
graph_2_path = sys.argv[4]

g_1 = nx.read_gexf(graph_1_path)
g_2 = nx.read_gexf(graph_2_path)

edges = {}

for p_1 in players:
    for s in possessions:
        e = '%s:%s' % (s, p_1)
        edges[e] = 0
    for p_2 in players:
        if p_1 == p_2:
            continue
        e = '%s:%s' % (p_1, p_2)
        edges[e] = 0
    for o in outcomes:
        e = '%s:%s' % (p_1, o)
        edges[e] = 0

for e in edges:
    u, v = e.split(':')
    w = 0
    w_1 = g_1.get_edge_data(u, v)
    w_2 = g_2.get_edge_data(u, v)
    if not w_1 is None:
        w += w_1['weight']
    if not w_2 is None:
        w += w_2['weight']
    edges[e] += w

g_out = nx.DiGraph()
for s in possessions:
    g_out.add_node(s)
for p in players:
    g_out.add_node(p)
for o in outcomes:
    g_out.add_node(o)

for e, w in edges.iteritems():
    u, v = e.split(':')
    g_out.add_weighted_edges_from([(u, v, w)])

nx.write_gexf(g_out, 'Graphs/%s-%d.gexf' % (team_name, season))
