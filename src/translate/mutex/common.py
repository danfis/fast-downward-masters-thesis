import networkx as nx
from itertools import combinations as comb

import common

def filter_atoms(atoms):
    atoms = [x for x in atoms if str(x).find('@') == -1]
    atoms = [x for x in atoms if str(x).find('Atom =') != 0]
    return set(atoms)

def create_atoms_dict(atoms):
    atoms = sorted(atoms)
    d = {a : i for i, a in enumerate(atoms) }
    return d, atoms

def atoms_to_keys(atoms, atoms_dict):
    keys = [atoms_dict[x] for x in atoms]
    return set(keys)

def gen_all_pairs(sets):
    pairs = [list(comb(s, 2)) for s in sets]
    if len(pairs) == 0:
        return set()

    pairs = reduce(lambda x, y: x + y, pairs)
    pairs = set([frozenset(x) for x in pairs])
    return pairs

def pair_mutexes(mutexes):
    return gen_all_pairs(mutexes)

def max_mutexes_from_pair_mutexes(pairs):
    if len(pairs) == 0:
        return set()

    pairs = [list(x) for x in pairs]
    atoms = reduce(lambda x, y: x + y, pairs)
    atoms_to_idx = {x:i for i, x in enumerate(atoms)}

    graph = nx.Graph()
    for pair in pairs:
        graph.add_edge(atoms_to_idx[pair[0]], atoms_to_idx[pair[1]])
    return set([frozenset([atoms[x] for x in c]) for c in nx.find_cliques(graph)])

def max_mutexes(mutexes):
    pairs = gen_all_pairs(mutexes)
    return max_mutexes_from_pair_mutexes(pairs)


class ExtendAction(object):
    def __init__(self, action, atoms):
        self.name = action.name
        self.pre = set(action.precondition) & atoms
        self.add_eff = set([x[1] for x in action.add_effects if len(x[0]) == 0])
        self.add_eff &= atoms
        self.del_eff = set([x[1] for x in action.del_effects if len(x[0]) == 0])
        self.del_eff &= atoms
        self.spurious = False
        # TODO: Conditional effects

class ExtendFact(object):
    def __init__(self, fact, pair_mutexes, actions):
        self.fact = fact
        self.mutex = set()
        self.add_action = set()
        self.del_action = set()

        for m in pair_mutexes:
            if fact in m:
                other = (set(m) - set([fact])).pop()
                self.mutex.add(other)

        for a in actions:
            if fact in a.add_eff:
                self.add_action.add(a)
            if fact not in a.del_eff:
                self.del_action.add(a)

    def check(self, f2):
        rel_actions = f2.add_action & self.del_action
        for a in rel_actions:
            if not a.spurious and len(a.pre & self.mutex) == 0:
                return False
        return True

    def add_mutex(self, f):
        self.mutex.add(f.fact)

class SpuriousDetector(object):
    def __init__(self, actions):
        self.dct = {}
        for a in actions:
            pairs = gen_all_pairs([a.pre, a.add_eff])
            for pair in pairs:
                if pair not in self.dct:
                    self.dct[pair] = set()
                self.dct[pair].add(a)

    def set_spurious(self, pairs):
        for pair in pairs:
            for a in self.dct.get(pair, set()):
                a.spurious = True
            self.dct.pop(pair, None)

    def exist(self, pair):
        return pair in self.dct

def extend_mutexes(mutexes, task, atoms, actions):
    atoms = common.filter_atoms(atoms)
    pairs = gen_all_pairs(mutexes)
    if len(pairs) == 0:
        return pairs

    actions = [ExtendAction(x, atoms) for x in actions]
    spurious = SpuriousDetector(actions)
    spurious.set_spurious(pairs)
    facts = { x : ExtendFact(x, pairs, actions) for x in atoms }

    candidates = gen_all_pairs([atoms]) - pairs
    init = set(task.init) & atoms
    candidates -= gen_all_pairs([init])

    candidates = set([frozenset([facts[x] for x in y]) for y in candidates])

    candidates_size = 0
    while candidates_size != len(candidates):
        candidates_size = len(candidates)
        for cand in list(candidates):
            pair = frozenset([x.fact for x in cand])
            if spurious.exist(pair):
                continue

            c1, c2 = cand
            if c1.check(c2) and c2.check(c1):
                spurious.set_spurious([pair])
                pairs.add(pair)
                candidates.remove(cand)
                c1.add_mutex(c2)
                c2.add_mutex(c1)
    return pairs, set()
