import itertools
import networkx as nx

def max_mutexes_from_pair_mutexes(pairs):
    atoms = reduce(lambda x, y: x + y, [list(x) for x in pairs])
    atoms_to_idx = {x:i for i, x in enumerate(atoms)}

    graph = nx.Graph()
    for pair in pairs:
        graph.add_edge(atoms_to_idx[pair[0]], atoms_to_idx[pair[1]])
    return [[atoms[x] for x in c] for c in nx.find_cliques(graph)]

def max_mutexes(mutexes):
    pairs = [list(itertools.combinations(m, 2)) for m in mutexes]
    pairs = reduce(lambda x, y: x + y, pairs)
    pairs = set([tuple(x) for x in pairs])
    return max_mutexes_from_pair_mutexes(pairs)
