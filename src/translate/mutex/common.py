import itertools
from itertools import combinations as comb
import networkx as nx

def gen_pair_mutexes(mutexes):
    pairs = [list(comb(m, 2)) for m in mutexes]
    pairs = reduce(lambda x, y: x + y, pairs)
    pairs = set([tuple(x) for x in pairs])
    return pairs

def max_mutexes_from_pair_mutexes(pairs):
    atoms = reduce(lambda x, y: x + y, [list(x) for x in pairs])
    atoms_to_idx = {x:i for i, x in enumerate(atoms)}

    graph = nx.Graph()
    for pair in pairs:
        graph.add_edge(atoms_to_idx[pair[0]], atoms_to_idx[pair[1]])
    return [[atoms[x] for x in c] for c in nx.find_cliques(graph)]

def max_mutexes(mutexes):
    pairs = gen_pair_mutexes(mutexes)
    return max_mutexes_from_pair_mutexes(pairs)


class ExtendAction(object):
    def __init__(self, action):
        self.name = action.name
        self.pre = set(action.precondition)
        self.add_eff = set([x[1] for x in action.add_effects if len(x[0]) == 0])
        self.del_eff = set([x[1] for x in action.del_effects if len(x[0]) == 0])
        # TODO: Conditional effects

class ExtendFact(object):
    def __init__(self, fact, pair_mutexes, actions):
        self.fact = fact
        self.mutex = set()
        self.add_action = set()
        self.del_action = set()

        for m in pair_mutexes:
            if fact in m:
                self.mutex.add(filter(lambda x: x != fact, m)[0])

        for a in actions:
            if fact in a.add_eff:
                self.add_action.add(a)
            if fact not in a.del_eff:
                self.del_action.add(a)

    def check(self, f2):
        rel_actions = f2.add_action & self.del_action
        for a in rel_actions:
            if len(a.pre & self.mutex) != 1:
                return False
        return True

    def add_mutex(self, f):
        self.mutex.add(f.fact)

def extend_mutexes(mutexes, task, atoms, actions):
    pairs = gen_pair_mutexes(mutexes)
    actions = [ExtendAction(x) for x in actions]
    facts = { x : ExtendFact(x, pairs, actions) for x in atoms }

    candidates = set([tuple(sorted(x)) for x in comb(atoms, 2)])
    candidates -= pairs
    candidates -= set([tuple(sorted(x)) for x in comb(task.init, 2)])
    for a in actions:
        candidates -= set([tuple(sorted(x)) for x in comb(a.add_eff, 2)])

    candidates = set([tuple([facts[x] for x in y]) for y in candidates])

    candidates_size = 0
    while candidates_size != len(candidates):
        candidates_size = len(candidates)
        for cand in candidates:
            if cand[0].check(cand[1]) and cand[1].check(cand[0]):
                pairs.add(tuple(sorted([x.fact for x in cand])))
                cand[0].add_mutex(cand[1])
                cand[1].add_mutex(cand[0])
        candidates -= pairs
    return pairs
