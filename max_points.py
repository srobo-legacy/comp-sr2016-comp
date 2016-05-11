#!/usr/bin/env python

from collections import defaultdict, Counter
from functools import partial
from itertools import chain
from pprint import pprint

from sr.comp.comp import SRComp

comp = SRComp('.')

all_scores = (comp.scores.tiebreaker, comp.scores.knockout, comp.scores.league)
all_points = dict(chain.from_iterable(s.game_points.items() for s in all_scores))

points_map = defaultdict(partial(defaultdict, list))

for match, points in all_points.items():
    for tla, team_points in points.items():
        points_map[team_points][tla].append(match)

for points, team_info in sorted(points_map.items()):
    print("{0} teams scored {1}".format(len(team_info), points))

max_points = max(points_map.keys())
max_points_infos = points_map[max_points]

pprint(dict(max_points_infos))
