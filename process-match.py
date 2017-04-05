import json
import networkx as nx
import os
import sys

file_in = open(sys.argv[1], 'r')

season = int(file_in.readline().strip())

season_teams_file_name = './Resources/season-%d-teams.json' % season
if not os.path.exists(season_teams_file_name):
    print('! ERROR: season teams file does not exist in json.')
    exit(0)

teams = None
with open(season_teams_file_name, 'r') as f_in:
    teams = json.loads(f_in.read().strip())

match = file_in.readline().strip()

blue_team = file_in.readline().strip()
orange_team = file_in.readline().strip()

blue_players = tuple(teams[blue_team])
orange_players = tuple(teams[orange_team])

match_name_tuple = (season, match, blue_team, orange_team)
match_file_name = './Data/s-%d-%s-%s-v-%s.csv' % match_name_tuple

match_file = open(match_file_name, 'w')
match_file.write('Game,U,V,Clock\n')

symbols = {
    'K': 'Kickoff',
    'I': 'Inbounds',
    'R': 'Rebound',
    '-': 'Steal',
    '+': 'Clear',
    '<': 'Yield',
    '#': 'Demo',
    '*': 'Score',
    '!': 'Save',
    '?': 'Miss',
    '$': 'Timeout',
    'A': blue_players[0],
    'B': blue_players[1],
    'C': blue_players[2],
    'X': orange_players[0],
    'Y': orange_players[1],
    'Z': orange_players[2]
}

edges = {}

game = 1
for line in file_in:
    line = line.strip()
    if line == '':
        continue
    if line == '$':
        game += 1
        continue
    move = line.split(' ')
    u, v, op, clock = None, None, None, None
    if len(move) == 3:
        u, v, clock = move
    elif len(move) == 4:
        u, v, op, clock = move
    t = int(clock) if clock.isdigit() else int(clock[1:])
    t = 60*(t / 100) + (t % 100)
    t = -t if clock.isdigit() else t
    if op is None:
        match_file.write("%s,%s,%s,%d\n" % (game, symbols[u], symbols[v], t))
        e = "%s:%s" % (u, v)
        if e in edges:
            edges[e] += 1
        else:
            edges[e] = 1
    else:
        match_file.write("%s,%s,%s,%d\n" % (game, symbols[u], symbols[op], t))
        match_file.write("%s,%s,%s,%d\n" % (game, symbols[op], symbols[v], t))
        e1 = "%s:%s" % (u, op)
        if e1 in edges:
            edges[e1] += 1
        else:
            edges[e1] = 1
        e2 = "%s:%s" % (v, op)
        if e2 in edges:
            edges[e2] += 1
        else:
            edges[e2] = 1

blue_g = nx.DiGraph()
orange_g = nx.DiGraph()

for s, node in symbols.iteritems():
    if s == 'X' or s == 'Y' or s == 'Z':
        continue
    blue_g.add_node(node)

for s, node in symbols.iteritems():
    if s == 'A' or s == 'B' or s == 'C':
        continue
    orange_g.add_node(node)

for e, weight in edges.iteritems():
    u, v = e.split(':')
    if (u == 'A' or u == 'B' or u == 'C') or (v == 'A' or v == 'B' or v == 'C'):
        blue_g.add_weighted_edges_from([(symbols[u], symbols[v], weight)])
    if (u == 'X' or u == 'Y' or u == 'Z') or (v == 'X' or v == 'Y' or v == 'Z'):
        orange_g.add_weighted_edges_from([(symbols[u], symbols[v], weight)])

nx.write_gexf(blue_g, 'Graphs/s-%d-%s-%s.gexf' % (season, match, blue_team))
nx.write_gexf(orange_g, 'Graphs/s-%d-%s-%s.gexf' % (season, match, orange_team))

match_file.close()
