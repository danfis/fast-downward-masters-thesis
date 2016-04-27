#!/usr/bin/env python

import sys
import subprocess
import os
import time
import itertools
from common import *

translate_path = '../translate.py'
paths = [ 'pddl-data/ipc-2008/seq-opt',
          'pddl-data/ipc-2011/seq-opt',
          'pddl-data/ipc-2014/seq-opt' ]
paths = [ 'pddl-data/ipc-2014/seq-opt' ]

def run(domain, problem, dom_pddl, problem_pddl, comb):
    outdir = 'out=' + ':'.join(comb)
    outfile = '{0}/{1}+{2}.out'.format(outdir, domain, problem)

    if os.path.isfile(outfile):
        return

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    mopt = '+'.join(comb)
    cmd = ['python2', translate_path, '--mutex', mopt, dom_pddl, problem_pddl]
    print(cmd)
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    out_fd = out.decode('ascii')

    open(outfile, 'w').write(out_fd)

def bench(domain, problem, dom_pddl, problem_pddl):
    print(domain, problem, dom_pddl, problem_pddl)
    mtype = ['fd', 'h2', 'fa', 'rfa', 'rfa-ilp', 'rfa-ilp-c']
    for m in mtype:
        run(domain, problem, dom_pddl, problem_pddl, [m])
        run(domain, problem, dom_pddl, problem_pddl, [m, 'extend'])
    return
    for size in range(1, len(mtype) + 1):
        for comb in itertools.combinations(mtype, size):
            for add in [[], ['extend']]:
                comb = list(comb) + add
                outdir = 'out=' + ':'.join(comb)
                if not os.path.isdir(outdir):
                    os.mkdir(outdir)
                mopt = '+'.join(comb)
                cmd = ['python2', translate_path, '--mutex', mopt, dom_pddl, problem_pddl]
                print(cmd)
                out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                out_fd = out.decode('ascii')

                outfile = '{0}/{1}+{2}.out'.format(outdir, domain, problem)
                open(outfile, 'w').write(out_fd)

#    outdir = 'out=full1000000'
#    if not os.path.isdir(outdir):
#        os.mkdir(outdir)
#    cmd = ['python2', translate_path, '--mutex', 'full1000000', dom_pddl, problem_pddl]
#    print(cmd)
#    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
#    out_fd = out.decode('ascii')
#    outfile = '{0}/{1}+{2}.out'.format(outdir, domain, problem)
#    open(outfile, 'w').write(out_fd)


def main(paths):
    for path in paths:
        for domdir in listDomainDirs(path):
            for prob, pddl, dom_pddl in pddlProblems(domdir):
                domain, problem = os.path.split(pddl)
                ipc, domain = os.path.split(domain)
                ipc, _ = os.path.split(ipc)
                _, ipc = os.path.split(ipc)

                if domain == 'citycar':
                    continue
                domain = domain + ':' + ipc[-2:]
                problem = problem[:-5]
                bench(domain, problem, dom_pddl, pddl)
#                try:
#                    bench(domain, problem, dom_pddl, pddl)
#                except:
#                    print('ERR:', domain, problem, dom_pddl, pddl)

if __name__ == '__main__':
    cmd = 'git clone https://github.com/danfis/pddl-data'
    os.system(cmd)
    main(paths)
