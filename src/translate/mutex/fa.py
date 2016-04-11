import cplex

import common

def fa(task, atoms, actions):
    atoms = common.filter_atoms(atoms)
    atoms_set = atoms
    atoms = list(atoms)
    atom_to_idx = dict(zip(atoms, range(len(atoms))))

    ilp = cplex.Cplex()
    ilp.objective.set_sense(ilp.objective.sense.maximize)
    ilp.set_log_stream(None)
    ilp.set_error_stream(None)
    ilp.set_results_stream(None)
    ilp.set_warning_stream(None)
    ilp.parameters.tune_problem([(ilp.parameters.threads, 1)])
    ilp.variables.add(obj = [1. for x in atoms],
                      names = [str(x) for x in atoms],
                      types = ['B' for x in atoms])

    # Initial state constraint
    s_init = list(set(task.init) & atoms_set)
    constr = cplex.SparsePair(ind = [atom_to_idx[x] for x in s_init],
                              val = [1. for _ in s_init])
    ilp.linear_constraints.add(lin_expr = [constr], senses = ['L'], rhs = [1.])

    # Action constraints
    for action in actions:
        pre = [atom_to_idx[x] for x in action.precondition if not x.negated]
        add_eff = [atom_to_idx[x[1]] for x in action.add_effects]
        del_eff = [atom_to_idx[x[1]] for x in action.del_effects]
        if len(add_eff) == 0:
            continue

        pre_del = list(set(pre) & set(del_eff))
        constr = cplex.SparsePair(ind = add_eff + pre_del,
                                  val = [1. for _ in add_eff]
                                        + [-1. for _ in pre_del])
        ilp.linear_constraints.add(lin_expr = [constr],
                                   senses = ['L'], rhs = [0.])

    mutexes = []
    ilp.solve()
    #print(c.solution.get_status())
    while ilp.solution.get_status() == 101:
        values = ilp.solution.get_values()
        if sum(values) <= 0.5:
            break
        sol = [atoms[x] for x in range(len(values)) if values[x] > 0.5]
        mutexes += [sol]

        # Add constraint removing all subsets of the current solution
        constr_idx = [x for x in range(len(values)) if values[x] < 0.5]
        constr = cplex.SparsePair(ind = constr_idx,
                                  val = [1. for _ in constr_idx])
        ilp.linear_constraints.add(lin_expr = [constr],
                                   senses = ['G'], rhs = [1.])
        ilp.solve()

    return mutexes
