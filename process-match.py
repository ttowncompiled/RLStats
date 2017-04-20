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

match = file_in.readline().strip().lower().replace(' ', '_')

blue_team = file_in.readline().strip().replace(' ', '_')
orange_team = file_in.readline().strip().replace(' ', '_')

blue_players = tuple(teams[blue_team])
orange_players = tuple(teams[orange_team])

match_name_tuple = (season, match, blue_team, orange_team)
match_file_name = './Out/s_%d-%s-%s-v-%s.csv' % match_name_tuple

match_file = open(match_file_name, 'w')
match_file.write('Game,U,V,Clock\n')

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
w = None
for line in file_in:
    line = line.strip()
    
    if line == '':
        continue
    if line == '$':
        game += 1
        continue
    
    if len(line.split(' ')) != 4:
        print('Invalid entry. Must have 4 components. (%s)' % (line))
        exit(0)
    
    u, v, op, clock = line.split(' ')
            
    if op == '#':
        continue
   
    t = int(clock) if clock.isdigit() else int(clock[1:])
    t = 60*(t / 100) + (t % 100)
    t = -t if clock.isdigit() else t

    if op == '=':
        if not (u == 'K' or u == 'I' or u == 'R') and u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if v == 'K' or v == 'I' or v == 'R':
            print('Invalid entry. v cannot be a possession for a pass. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'A' or u == 'B' or u == 'C') and (v == 'X' or v == 'Y' or v == 'Z'):
            print('Invalid entry. Opponents cannot pass to each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'X' or u == 'Y' or u == 'Z') and (v == 'A' or v == 'B' or v == 'C'):
            print('Invalid entry. Opponents cannot pass to each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = v
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[v], t))
        e1 = "%s:%s" % (u, v)
        if e1 in edges:
            edges[e1] += 1
        else:
            edges[e1] = 1
    elif op == '-':
        if u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if u == 'K' or u == 'I' or u == 'R':
            print('Invalid entry. u cannot be a possession for a steal. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if v == 'K' or v == 'I' or v == 'R':
            print('Invalid entry. v cannot be a possession for a steal. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'A' or u == 'B' or u == 'C') and (v == 'A' or v == 'B' or v == 'C'):
            print('Invalid entry. Teammates cannot steal from each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'X' or u == 'Y' or u == 'Z') and (v == 'Z' or v == 'Y' or v == 'Z'):
            print('Invalid entry. Teammates cannot steal from each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = v
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[op], t))
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[op], symbols[v], t))
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
    elif op == '+':
        if u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if u == 'K' or u == 'I' or u == 'R':
            print('Invalid entry. u cannot be a possession for a clear. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if v == 'K' or v == 'I' or v == 'R':
            print('Invalid entry. v cannot be a possession for a clear. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'A' or u == 'B' or u == 'C') and (v == 'A' or v == 'B' or v == 'C'):
            print('Invalid entry. Teammates cannot clear from each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'X' or u == 'Y' or u == 'Z') and (v == 'Z' or v == 'Y' or v == 'Z'):
            print('Invalid entry. Teammates cannot clear from each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = v
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[op], t))
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[op], symbols[v], t))
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
    elif op == '/':
        if u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if u == 'K' or u == 'I' or u == 'R':
            print('Invalid entry. u cannot be a possession for a yield. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if v != '/':
            print('Invalid entry. v must be / for a yield. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = None
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[op], t))
        e1 = "%s:%s" % (u, op)
        if e1 in edges:
            edges[e1] += 1
        else:
            edges[e1] = 1
    elif op == '*':
        if u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if u == 'K' or u == 'I' or u == 'R':
            print('Invalid entry. u cannot be a possession for a score. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if v != '*':
            print('Invalid entry. v must be * for a score. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = None
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[op], t))
        e1 = "%s:%s" % (u, op)
        if e1 in edges:
            edges[e1] += 1
        else:
            edges[e1] = 1
    elif op == '!':
        if u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if u == 'K' or u == 'I' or u == 'R':
            print('Invalid entry. u cannot be a possession for a save. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if v == 'K' or v == 'I' or v == 'R':
            print('Invalid entry. v cannot be a possession for a save. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'A' or u == 'B' or u == 'C') and (v == 'A' or v == 'B' or v == 'C'):
            print('Invalid entry. Teammates cannot save from each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if (u == 'X' or u == 'Y' or u == 'Z') and (v == 'Z' or v == 'Y' or v == 'Z'):
            print('Invalid entry. Teammates cannot save from each other. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = None
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[op], t))
        e1 = "%s:%s" % (u, op)
        if e1 in edges:
            edges[e1] += 1
        else:
            edges[e1] = 1
    elif op == '?':
        if u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if u == 'K' or u == 'I' or u == 'R':
            print('Invalid entry. u cannot be a possession for a miss. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if v != '?':
            print('Invalid entry. v must be ? for a miss. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = None
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[op], t))
        e1 = "%s:%s" % (u, op)
        if e1 in edges:
            edges[e1] += 1
        else:
            edges[e1] = 1
    elif op == '$':
        if u != w:
            print('Invalid entry. u != w. (%s, %s, %s, %s, %s)' % (w, u, v, op, clock))
            exit(0)
        if u == 'K' or u == 'I' or u == 'R':
            print('Invalid entry. u cannot be a possession for a stop. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        if v != '$':
            print('Invalid entry. v must be $ for a stop. (%s, %s, %s, %s)' % (u, v, op, clock))
            exit(0)
        w = None
        match_file.write('%s,%s,%s,%d\n' % (game, symbols[u], symbols[op], t))
        e1 = "%s:%s" % (u, op)
        if e1 in edges:
            edges[e1] += 1
        else:
            edges[e1] = 1
    else:
        print('Invalid entry. Unrecognized op. (%s, %s, %s, %s)' % (u, v, op, clock))
        exit(0)

file_in.close()

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

nx.write_gexf(blue_g, 'Out/s_%d-%s-%s.gexf' % (season, match, blue_team))
nx.write_gexf(orange_g, 'Out/s_%d-%s-%s.gexf' % (season, match, orange_team))

match_file.close()
