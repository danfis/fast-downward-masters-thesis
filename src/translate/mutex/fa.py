import cplex

import common

def fa(task, atoms, actions, rfa = False):
    atoms = common.filter_atoms(atoms)
    atoms_dict, atoms_list = common.create_atoms_dict(atoms)

    ilp = cplex.Cplex()
    ilp.objective.set_sense(ilp.objective.sense.maximize)
    ilp.set_log_stream(None)
    ilp.set_error_stream(None)
    ilp.set_results_stream(None)
    ilp.set_warning_stream(None)
    ilp.parameters.tune_problem([(ilp.parameters.threads, 1)])
    ilp.variables.add(obj = [1. for x in atoms_list],
                      names = [str(x) for x in atoms_list],
                      types = ['B' for x in atoms_list])

    # Initial state constraint
    s_init = list(set(task.init) & atoms)
    constr = cplex.SparsePair(ind = [atoms_dict[x] for x in s_init],
                              val = [1. for _ in s_init])
    ilp.linear_constraints.add(lin_expr = [constr], senses = ['L'], rhs = [1.])

    # Action constraints
    for action in actions:
        pre = set(action.precondition) & atoms
        add_eff = set([x[1] for x in action.add_effects]) & atoms
        del_eff = set([x[1] for x in action.del_effects]) & atoms
        pre = [atoms_dict[x] for x in pre if not x.negated]
        add_eff = [atoms_dict[x] for x in add_eff]
        del_eff = [atoms_dict[x] for x in del_eff]
        if len(add_eff) == 0:
            continue

        pre_del = list(set(pre) & set(del_eff))
        constr = cplex.SparsePair(ind = add_eff + pre_del,
                                  val = [1. for _ in add_eff]
                                        + [-1. for _ in pre_del])
        ilp.linear_constraints.add(lin_expr = [constr],
                                   senses = ['L'], rhs = [0.])
        if rfa:
            constr2 = cplex.SparsePair(ind = pre_del, val = [1. for _ in pre_del])
            ilp.linear_constraints.add(lin_expr = [constr2],
                                       senses = ['L'], rhs = [1.])

    mutexes = set()
    ilp.solve()
    #print(c.solution.get_status())
    while ilp.solution.get_status() == 101:
        values = ilp.solution.get_values()
        if sum(values) <= 1.5:
            break
        sol = [atoms_list[x] for x in range(len(values)) if values[x] > 0.5]
        mutexes.add(frozenset(sol))

        # Add constraint removing all subsets of the current solution
        constr_idx = [x for x in range(len(values)) if values[x] < 0.5]
        constr = cplex.SparsePair(ind = constr_idx,
                                  val = [1. for _ in constr_idx])
        ilp.linear_constraints.add(lin_expr = [constr],
                                   senses = ['G'], rhs = [1.])
        ilp.solve()

    return mutexes, set()
