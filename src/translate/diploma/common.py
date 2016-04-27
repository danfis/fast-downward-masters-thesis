import sys
import os
import hashlib

def findDuplicates(paths):
    hash_files = {}
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                with open(full_path, 'rb') as fin:
                    h = hashlib.sha224(fin.read()).hexdigest()
                    if h in hash_files:
                        hash_files[h] += [full_path]
                    else:
                        hash_files[h] = [full_path]

    duplicates = []
    for key, full_paths in hash_files.items():
        if len(full_paths) > 1:
            duplicates += [sorted(full_paths)]
    duplicates = sorted(duplicates)

    for dup in duplicates:
        print(' '.join(dup))

def listDomainDirs(path):
    dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        fs = [x for x in filenames if x[-5:] == '.pddl']
        if len(fs) > 0:
            dirs += [dirpath]
    return sorted(dirs)

def domainDirs(d):
    dirs = os.listdir(d)
    dirs = [(x.lower(), os.path.join(d, x)) for x in dirs]
    dirs = filter(lambda x: os.path.isdir(x[1]), dirs)
    dirs = sorted(dirs)
    return dirs

def problemDirs(d):
    dirs = os.listdir(d)
    dirs = [(x, os.path.join(d, x)) for x in dirs]
    dirs = filter(lambda x: os.path.isdir(x[1]), dirs)
    dirs = sorted(dirs)
    return dirs

def pddlFiles(d):
    files = os.listdir(d)
    files = sorted(filter(lambda x: x[-5:] == '.pddl', files))
    files = [(x, os.path.join(d, x)) for x in files]
    return files

def pddlMAProblems(d):
    files = os.listdir(d)
    files = filter(lambda x: x[-5:] == '.pddl', files)
    files = filter(lambda x: x.startswith('problem-'), files)
    names = [x[8:-5] for x in files]
    names = sorted(names)
    for i, name in enumerate(names):
        dom_pddl = os.path.join(d, 'domain-' + name + '.pddl')
        pddl = os.path.join(d, 'problem-' + name + '.pddl')
        yield i, name, dom_pddl, pddl

def pddlProblems(d):
    files = os.listdir(d)
    files = filter(lambda x: x.find('domain') == -1, files)
    pddls = filter(lambda x: x[-5:] == '.pddl', files)
    names = sorted([x[:-5] for x in pddls])
    for n in names:
        pddl = os.path.join(d, n + '.pddl')
        if not os.path.isfile(pddl):
            continue

        domain = os.path.join(d, 'domain_' + n + '.pddl')
        if os.path.isfile(domain):
            yield n, pddl, domain

        if n.find('problem') != -1:
            domain = os.path.join(d, n.replace('problem', 'domain') + '.pddl')
            if os.path.isfile(domain):
                yield n, pddl, domain

        domain = os.path.join(d, n + '-domain.pddl')
        if os.path.isfile(domain):
            yield n, pddl, domain

        domain = os.path.join(d, 'domain.pddl')
        if os.path.isfile(domain):
            yield n, pddl, domain
