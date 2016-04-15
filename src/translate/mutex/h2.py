import sys
import itertools
from pprint import pprint

import common

def gen_pair_meta_atoms(atoms):
    return [tuple(sorted(x)) for x in itertools.combinations(atoms, 2)]

def gen_meta_atoms(atoms):
    ma = [x for x in atoms]
    ma += gen_pair_meta_atoms(atoms)
    return ma

class P2Action(object):
    def __init__(self, name, pre, add_eff, add_fact = None):
        self.name = name
        if add_fact is None:
            add_fact = []
        else:
            self.name += '+' + str(add_fact)
            add_fact = [add_fact]

        self.pre = set(gen_meta_atoms(set(pre + add_fact)))
        self.add = set(gen_meta_atoms(set(add_eff + add_fact)))
        if len(add_fact) > 0:
            self.add = self.add - set(add_fact)

        self.add = self.add - self.pre

def create_p2_actions(actions, atoms):
    p2 = []
    for a in actions:
        pre = a.precondition
        add_eff = [x[1] for x in a.add_effects if len(x[0]) == 0]
        del_eff = [x[1] for x in a.del_effects if len(x[0]) == 0]
        exp = atoms - (set(add_eff) | set(del_eff))
        # TODO: Conditional effects

        p2 += [P2Action(a.name, pre, add_eff)]
        for fact in exp:
            p2 += [P2Action(a.name, pre, add_eff, fact)]

    return p2

def h2p2(task, atoms, actions):
    atoms = common.filter_atoms(atoms)
    actions = create_p2_actions(actions, atoms)

    lastsize = 0
    reached = set(gen_meta_atoms(set(task.init) & atoms))
    while len(reached) != lastsize:
        lastsize = len(reached)

        next_actions = []
        for a in actions:
            if a.pre.issubset(reached):
                reached |= a.add
            else:
                next_actions += [a]
        actions = next_actions

    h2_mutex = set(gen_pair_meta_atoms(atoms)) - reached
    unreachable = atoms - reached
    return h2_mutex, unreachable

class H2Action(object):
    def __init__(self, a):
        self.name = a.name

        pre = a.precondition
        add_eff = [x[1] for x in a.add_effects if len(x[0]) == 0]
        del_eff = [x[1] for x in a.del_effects if len(x[0]) == 0]
        self.pre1 = set(pre)
        self.add_eff1 = set(add_eff)
        self.add_del = set(add_eff) | set(del_eff)

        self.pre2 = set(gen_pair_meta_atoms(self.pre1))
        p = self.pre1 - self.add_del
        self.add_eff2 = set(gen_pair_meta_atoms(self.add_eff1 | p))

        self.pre = self.pre1 | self.pre2
        self.add_eff = self.add_eff1 | self.add_eff2

    def pairs(self, fact, facts):
        for f in facts:
            yield tuple(sorted([fact, f]))

    def eff(self, reached):
        h2 = set(self.add_eff)

        atoms = set([x for x in reached if type(x) is not tuple])
        atoms -= self.add_del
        for atom in atoms:
            pre = set(self.pairs(atom, self.pre1))
            if pre.issubset(reached):
                for atom2 in self.add_eff1:
                    t = tuple(sorted([atom, atom2]))
                    h2.add(t)
        return h2


def h2(task, atoms, actions):
    atoms = common.filter_atoms(atoms)
    actions = [H2Action(a) for a in actions]

    lastsize = 0
    init = set(task.init) & atoms
    reached = set(gen_meta_atoms(init))
    while len(reached) != lastsize:
        lastsize = len(reached)

        for a in actions:
            if a.pre.issubset(reached):
                reached |= a.eff(reached)

    h2 = set(gen_meta_atoms(atoms)) - reached
    h1 = set([x for x in h2 if type(x) is not tuple])
    h2 -= h1
    h2 |= set([tuple([x]) for x in h1])
    return list(h2)

def h2_max(task, atoms, actions):
    h2_mutex, unreachable = h2(task, atoms, actions)
    return common.max_mutexes_from_pair_mutexes(h2_mutex)

