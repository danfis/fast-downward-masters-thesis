import cplex
from itertools import combinations as comb

import common

class RFAAction(object):
    def __init__(self, action, atom_to_fact):
        self.name = action.name
        self.pre = set([atom_to_fact[x] for x in action.precondition if not x.negated])
        self.add_eff = set([atom_to_fact[x[1]] for x in action.add_effects])
        self.del_eff = set([atom_to_fact[x[1]] for x in action.del_effects])
        self.pre_del = self.pre & self.del_eff

class RFAFact(object):
    def __init__(self, fact, atoms):
        self.fact = fact
        self.all_facts = None
        self.actions = None

        self.bind = set([self])
        self.conflict = set()
        self.useless = False

    def set_all_facts(self, facts):
        self.all_facts = facts
    def set_actions(self, actions):
        self.actions = actions

    def add_conflict(self, f2):
        if f2 not in self.conflict:
            self.conflict.add(f2)
            f2.conflict.add(self)
            return True
        return False

    def add_bind(self, f2):
        if f2.useless:
            self.set_useless()
            return True

        elif f2 not in self.bind:
            self.bind.add(f2)
            return True
        return False

    def set_useless(self):
        if not self.useless:
            self.useless = True
            for f in self.all_facts:
                self.add_bind(f)
                self.add_conflict(f)
            return True

        return False

    def apply_transitivity(self):
        if self.useless:
            return False

        change = False
        for f2 in set(self.bind):
            for f3 in f2.bind:
                change |= self.add_bind(f3)
            for f3 in set(f2.conflict):
                change |= self.add_conflict(f3)
        return change

    def check_useless(self):
        if not self.useless and len(self.bind & self.conflict) > 0:
            return self.set_useless()
        return False

    def check_actions(self):
        if self.useless:
            return False

        change = False
        pre_del = set()
        for a in self.actions:
            if len(a.add_eff & self.bind) > 0:
                pd = a.pre_del - self.conflict
                if len(pd) == 0:
                    return self.set_useless()
                if len(pd) == 1:
                    change |= self.add_bind(list(pd)[0])
                pre_del.add(frozenset(pd))

        for pd1, pd2 in comb(pre_del, 2):
            if pd1.issubset(pd2):
                for f in pd2 - pd1:
                    change |= self.add_conflict(f)
            if pd2.issubset(pd1):
                for f in pd1 - pd2:
                    change |= self.add_conflict(f)

        return change

    def check_rfa(self):
        for a in self.actions:
            add_size = len(a.add_eff & self.bind)
            pre_del_size = len(a.pre_del & self.bind)
            if add_size > 1 or pre_del_size > 1 or pre_del_size > add_size:
                return False
        return True


def rfa_init(atom_to_fact, task, atoms, actions):
    s_init = [atom_to_fact[x] for x in set(task.init) & set(atoms)]
    for f1, f2 in comb(s_init, 2):
        f1.add_conflict(f2)

    for a in actions:
        for f1, f2 in comb(a.add_eff, 2):
            f1.add_conflict(f2)
        for f1, f2 in comb(a.pre_del, 2):
            f1.add_conflict(f2)


def rfa_conflict_bind(task, atoms, actions):
    atoms = common.filter_atoms(atoms)
    atom_to_fact = { a : RFAFact(a, atoms) for a in atoms }
    facts = atom_to_fact.values()
    actions = [RFAAction(a, atom_to_fact) for a in actions]
    [(f.set_all_facts(facts), f.set_actions(actions)) for f in facts]

    rfa_init(atom_to_fact, task, atoms, actions)

    change = True
    while change:
        change = False
        for f in facts:
            change |= f.apply_transitivity()
            change |= f.check_useless()
            change |= f.check_actions()
    return facts

def rfa(task, atoms, actions):
    facts = rfa_conflict_bind(task, atoms, actions)
    rfa = set()
    for f in facts:
        if f.check_rfa():
            rfa.add(frozenset([x.fact for x in f.bind]))
    rfa = [list(x) for x in rfa]
    return rfa

def rfa_complete(task, atoms, actions):
    facts = rfa_conflict_bind(task, atoms, actions)
    facts = [f for f in facts if not f.useless]
    fact_to_idx = { x.fact : i for i, x in enumerate(facts) }
    fact_to_idx2 = { x : i for i, x in enumerate(facts) }

    ilp = cplex.Cplex()
    ilp.objective.set_sense(ilp.objective.sense.maximize)
    ilp.set_log_stream(None)
    ilp.set_error_stream(None)
    ilp.set_results_stream(None)
    ilp.set_warning_stream(None)
    ilp.parameters.tune_problem([(ilp.parameters.threads, 1)])
    ilp.variables.add(obj = [1. for x in facts],
                      names = [str(x.fact) for x in facts],
                      types = ['B' for x in facts])

    # Initial state constraint
    s_init = list(set(task.init) & set([x.fact for x in facts]))
    constr = cplex.SparsePair(ind = [fact_to_idx[x] for x in s_init],
                              val = [1. for _ in s_init])
    ilp.linear_constraints.add(lin_expr = [constr], senses = ['L'], rhs = [1.])

    # Action constraints
    for action in facts[0].actions:
        add_eff = [fact_to_idx2[x] for x in action.add_eff]
        pre_del = [fact_to_idx2[x] for x in action.pre_del]

        constr = cplex.SparsePair(ind = add_eff + pre_del,
                                  val = [1. for _ in add_eff]
                                        + [-1. for _ in pre_del])
        constr2 = cplex.SparsePair(ind = pre_del, val = [1. for _ in pre_del])
        ilp.linear_constraints.add(lin_expr = [constr, constr2],
                                   senses = ['L', 'L'], rhs = [0., 1.])

    # Bind and conflict set constraints
    for f in facts:
        bind = [fact_to_idx2[x] for x in f.bind - set([f])]
        cbind = cplex.SparsePair(ind = bind + [fact_to_idx2[f]],
                                 val = [-1. for _ in bind] + [len(bind)])

        confl = [fact_to_idx2[x] for x in f.conflict]
        cconfl = cplex.SparsePair(ind = confl + [fact_to_idx2[f]],
                                  val = [1. for _ in confl] + [len(confl)])
        ilp.linear_constraints.add(lin_expr = [cbind, cconfl],
                                   senses = ['L', 'L'], rhs = [0., len(confl)])

    mutexes = []
    ilp.solve()
    #print(c.solution.get_status())
    while ilp.solution.get_status() == 101:
        values = ilp.solution.get_values()
        if sum(values) <= 0.5:
            break
        sol = [facts[x].fact for x in range(len(values)) if values[x] > 0.5]
        mutexes += [sol]

        # Add constraint removing all subsets of the current solution
        constr_idx = [x for x in range(len(values)) if values[x] < 0.5]
        constr = cplex.SparsePair(ind = constr_idx,
                                  val = [1. for _ in constr_idx])
        ilp.linear_constraints.add(lin_expr = [constr],
                                   senses = ['G'], rhs = [1.])
        ilp.solve()

    return mutexes
