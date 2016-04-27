#!/usr/bin/env python

import sys
import os
import pprint
import itertools
import pickle
import scipy.stats
import numpy
from pprint import pprint


_full = [
    ('barman', 'p433.1'),
    ('ged', 'd-1-2'),
    ('hiking', 'ptesting-1-2-3'),
    ('maintenance', 'maintenance.1.3.010.010.1-001'),
    ('tetris', 'p01-4'),
    ('transport', 'p01'),
    ('visitall', 'p-1-5'),
]

gnuplot_scatter_m2 = '''
set grid
set xlabel "{0}" font ",15"
set ylabel "{1}" font ",15"

#set terminal epslatex color
#set output "tmp.tex"
set terminal pdfcairo color size 2.3,2
set output "m2_scatter_{2}_{3}.pdf"

set style line 80 lt rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80

set logscale x 10
set logscale y 10
set xtics ("0" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000, "10^4" 10000, "10^5" 100000, "10^6" 1000000)
set ytics ("0" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000, "10^4" 10000, "10^5" 100000, "10^6" 1000000)
set xtics nomirror
set ytics nomirror


set style rect back fc rgb "white" fs solid border lc rgb "#ffffff" lw 2
set object 1 rect from 0.20,0.05 to 0.35,1000000
set arrow 1 from 0.19,0.035 to 0.19,0.07 nohead lw 1 lc rgb "#808080" back
set arrow 2 from 0.37,0.035 to 0.37,0.07 nohead lw 1 lc rgb "#808080" back
set object 2 rect from 0.05,0.20 to 1000000,0.35
set arrow 3 from 0.035,0.19 to 0.07,0.19 nohead lw 1 lc rgb "#808080" back
set arrow 4 from 0.035,0.37 to 0.07,0.37 nohead lw 1 lc rgb "#808080" back

set arrow 5 from 0.19,0.19 to .36,.36 nohead lw 2 lc rgb "#ffffff" front
set arrow 6 from 0.19,0.19 to .36,.36 nohead lt 0 lc rgb "#000000" front
set arrow 7 from 0.21,0.21 to .36,.36 nohead lt 0 lc rgb "#000000" front


set yrange [0.05:1000000]
set xrange [0.05:1000000]
plot x notitle w l lw 1 black, \\
     "m2_scatter_{2}_{3}.data" notitle w p ps 1 black
'''

gnuplot_scatter_m_ = '''
set grid
set xlabel "{0}" font ",15"
set ylabel "{1}" font ",15"

#set terminal epslatex color
#set output "tmp.tex"
set terminal pdfcairo color size 2.3,2
set output "m_scatter_{2}_{3}.pdf"

set style line 80 lt rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80

set logscale x 10
set logscale y 10
if ("{2}" eq "fd") && ("{3}" eq "rfa") \\
set yrange [-1:60]; \\
set xrange [-1:60]; \\
else \\
set yrange [-1:100]; \\
set xrange [-1:100]

set xtics (0, 20, 40, 60, 80, 100)
set ytics (0, 20, 40, 60, 80, 100)
set xtics nomirror
set ytics nomirror

plot x notitle w l lw 1 black, \\
     "m_scatter_{2}_{3}.data" notitle w p ps 1 black
'''

gnuplot_scatter_m = '''
set grid
set xlabel "{0}" font ",15"
set ylabel "{1}" font ",15"

#set terminal epslatex color
#set output "tmp.tex"
set terminal pdfcairo color size 2.3,2
set output "m_scatter_{2}_{3}.pdf"

set style line 80 lt rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80

set logscale x 10
set logscale y 10
set xtics ("0" 0.7, "1" 1, "2" 2, "5" 5, "10" 10, "20" 20, "50" 50, "100" 100)
set ytics ("0" 0.7, "1" 1, "2" 2, "5" 5, "10" 10, "20" 20, "50" 50, "100" 100)
set xtics nomirror
set xtics nomirror
set ytics nomirror


set style rect back fc rgb "white" fs solid border lc rgb "#ffffff" lw 2
set object 1 rect from 0.80,0.05 to 0.85,1000000
set arrow 1 from 0.79,0.60 to 0.79,0.7 nohead lw 1 lc rgb "#808080" back
set arrow 2 from 0.87,0.60 to 0.87,0.7 nohead lw 1 lc rgb "#808080" back
set object 2 rect from 0.05,0.80 to 1000000,0.85
set arrow 3 from 0.60,0.79 to 0.7,0.79 nohead lw 1 lc rgb "#808080" back
set arrow 4 from 0.60,0.87 to 0.7,0.87 nohead lw 1 lc rgb "#808080" back

set arrow 5 from 0.79,0.79 to .86,.86 nohead lw 2 lc rgb "#ffffff" front
set arrow 6 from 0.79,0.79 to .86,.86 nohead lt 0 lc rgb "#000000" front
set arrow 7 from 0.71,0.71 to .86,.86 nohead lt 0 lc rgb "#000000" front


set yrange [0.65:100]
set xrange [0.65:100]
plot x notitle w l lw 1 black, \\
     "m_scatter_{2}_{3}.data" notitle w p ps 1 black
'''

gnuplot_scatter_var = '''
set grid
set xlabel "{0}" font ",15"
set ylabel "{1}" font ",15"

#set terminal epslatex color
#set output "tmp.tex"
set terminal pdfcairo color size 2.3,2
set output "var_scatter_{2}_{3}.pdf"

set style line 80 lt rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80

set logscale x 10
set logscale y 10
set xtics ("1" 1, "10" 10, "10^2" 100, "10^3" 1000)
set ytics ("1" 1, "10" 10, "10^2" 100, "10^3" 1000)
set xtics nomirror
set ytics nomirror

set yrange [0.9:2000]
set xrange [0.9:2000]
plot x notitle w l lw 1 black, \\
     "var_scatter_{2}_{3}.data" notitle w p ps 1 black
'''

gnuplot_scatter_m2_time = '''
set grid
set xlabel "{0} (s)" font ",15"
set ylabel "{1} (s)" font ",15"

#set terminal epslatex color
#set output "tmp.tex"
set terminal pdfcairo color size 2.3,2
set output "m2_time_scatter_{2}_{3}.pdf"

set style line 80 lt rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80

set logscale x 10
set logscale y 10
set xtics ("0.01" 0.01, "0.1" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000)
set ytics ("0.01" 0.01, "0.1" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000)
set xtics nomirror
set ytics nomirror


set yrange [0.008:2000]
if ("{2}" eq "fd") \\
set xrange [0.008:1]; \\
else \\
set xrange [0.008:2000]
plot x notitle w l lw 1 black, \\
     "m2_time_scatter_{2}_{3}.data" notitle w p ps 1 black
'''

gnuplot_scatter_var_time = '''
set grid
set xlabel "{0} (s)" font ",15"
set ylabel "{1} (s)" font ",15"

#set terminal epslatex color
#set output "tmp.tex"
set terminal pdfcairo color size 2.3,2
set output "var_time_scatter_{2}_{3}.pdf"

set style line 80 lt rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80

set logscale x 10
set logscale y 10
set xtics ("0.01" 0.01, "0.1" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000)
set ytics ("0.01" 0.01, "0.1" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000)
set xtics nomirror
set ytics nomirror

if ("{2}" eq "fd") set xrange [0.008:15]
if ("{2}" eq "fa") set xrange [0.008:100]
if ("{3}" eq "fa") set yrange [0.008:100]
if ("{3}" eq "rfa") set yrange [0.008:1200]
plot x notitle w l lw 1 black, \\
     "var_time_scatter_{2}_{3}.data" notitle w p ps 1 black
'''

gnuplot_scatter_num_vars = '''
set grid
set xlabel "{0}" font ",15"
set ylabel "{1}" font ",15"

#set terminal epslatex color
#set output "tmp.tex"
set terminal pdfcairo color size 2.3,2
set output "vars_scatter_{2}_{3}.pdf"

set style line 80 lt rgb "#808080"
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80
set xtics ("0" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000, "10^4" 10000)
set ytics ("0" 0.1, "1" 1, "10" 10, "10^2" 100, "10^3" 1000, "10^4" 10000)
set xtics nomirror
set ytics nomirror

set logscale x 10
set logscale y 10
set yrange [0.9:10000]
set xrange [0.9:10000]
plot x notitle w l lw 1 black, \\
     "vars_scatter_{2}_{3}.data" notitle w p ps 1 black
'''

def texName(m):
    E = False
    if m.endswith(':extend'):
        E = True
        m, _ = m.split(':')
    if m == 'h2':
        m = 'h$^2$'
    if E:
        m = 'E[' + m + ']'
    return m

def plotName(m):
    E = False
    if m.endswith(':extend'):
        E = True
        m, _ = m.split(':')
    if m == 'h2':
        m = 'h^2'
    if E:
        m = 'E[' + m + ']'
    return m

class Data(object):
    def __init__(self):
        self.data = None
        self.full = None

        self.facts = []
        self.facts_dict = {}
        self.mutexes = []
        self.mutexes_dict = {}

    def load(self):
        if os.path.isfile('data.pickle'):
            with open('data.pickle', 'rb') as fin:
                d = pickle.load(fin)
                self.data = d.data
                self.full = d.full
                self.facts = d.facts
                self.facts_dict = d.facts_dict
                self.mutexes = d.mutexes
                self.mutexes_dict = d.mutexes_dict

        else:
            self.loadFull()
            self.loadData()
            with open('data.pickle', 'wb') as fout:
                pickle.dump(self, fout)

    def loadFull(self):
        self.full = []
        for domain, problem in _full:
            d = [domain, problem, set(), set()]
            lines = open('full/{0}/m.out'.format(domain), 'r').read().split('\n')
            for line in lines:
                if ';' not in line:
                    d[3].add(self._fact(line))
                else:
                    m1, m2 = line.split(';')
                    d[2].add(self._mutex([m1, m2]))
            self.full += [d]

    def _fact(self, name):
        if name not in self.facts_dict:
            idx = len(self.facts)
            self.facts += [name]
            self.facts_dict[name] = idx
        return self.facts_dict[name]

    def _mutex(self, m):
        m = [self._fact(x) for x in m]
        m = frozenset(m)

        if m not in self.mutexes_dict:
            idx = len(self.mutexes)
            self.mutexes += [m]
            self.mutexes_dict[m] = idx
        return self.mutexes_dict[m]

    def _printMutex(self, idx):
        m = self.mutexes[idx]
        print('M:', idx, m, [self.facts[x] for x in m])

    def _removeSubsets(self, ms):
        out = []
        ss = [frozenset(x) for x in ms]
        ss = sorted(ss, key = lambda x: -len(x))
        for s in ss:
            add = True
            for x in out:
                if s.issubset(x):
                    add = False
                    break
            if add:
                out += [s]
        return [self._mutex(x) for x in out]

    def loadDataFile(self, mtype, fn):
        out = { 'mutex' : [],
                'mutex2' : [],
                'mutex-max' : [],
                'mutex-time' : None,
                'time1' : None,
                'time2' : None,
                'num-vars' : None,
                'num-facts' : None,
              }

        data = open(fn, 'r').read().split('\n')
        for line in data:
            if line.startswith('MUTEX:'):
                m = line[7:].split(';')
                #out['mutex'] += [self._mutex(m)]
                out['mutex'] += [m]

            elif line.startswith('MUTEX2:'):
                m = line[8:].split(';')
                out['mutex2'] += [self._mutex(m)]

            elif line.startswith('MUTEX-MAX:'):
                m = line[11:].split(';')
                out['mutex-max'] += [self._mutex(m)]

            elif line.startswith('MUTEX TIME:'):
                out['mutex-time'] = float(line.split(': ')[1])

            elif line.startswith('Time1:'):
                out['time1'] = float(line.split(': ')[1])

            elif line.startswith('Time2:'):
                out['time2'] = float(line.split(': ')[1])

            elif line.startswith('Translator variables:'):
                out['num-vars'] = int(line.split(': ')[1])

            elif line.startswith('Translator facts:'):
                out['num-facts'] = int(line.split(': ')[1])

        if mtype in ['fd', 'rfa']:
            out['mutex'] = self._removeSubsets(out['mutex'])
        else:
            out['mutex'] = [self._mutex(x) for x in out['mutex']]
        return out

    def loadData1(self, mtype):
        out = {}

        d = 'out=' + mtype
        for fn in os.listdir(d):
            domain, problem = fn.split('+')
            problem = problem[:-4]
            domain, year = domain.split(':')
            if year != '14':
                continue

            print(domain, year, problem, fn)
            if domain not in out:
                out[domain] = {}

            out[domain][problem] = self.loadDataFile(mtype, d + '/' + fn)

        return out

    def loadData(self):
        mtype = ['fd', 'h2', 'fa', 'rfa', 'rfa-ilp', 'rfa-ilp-c']
        mtype += [x + ':extend' for x in mtype]
        self.data = { m : self.loadData1(m) for m in mtype }

    def domains(self):
        return sorted(self.data['fd'].keys())

    def problems(self, dom):
        return sorted(self.data['fd'][dom].keys())

    def tupleDom(self, dom, ms):
        for prob in self.problems(dom):
            yield {x : self.data[x][dom][prob] for x in ms}

    def pair(self, m1, m2):
        for dom in self.data[m1].keys():
            for prob in self.data[m1][dom].keys():
                d1 = self.data[m1][dom][prob]
                d2 = self.data[m2][dom][prob]
                yield d1, d2

    def triplet(self, m1, m2, m3):
        for dom in self.data[m1].keys():
            for prob in self.data[m1][dom].keys():
                d1 = self.data[m1][dom][prob]
                d2 = self.data[m2][dom][prob]
                d3 = self.data[m3][dom][prob]
                yield d1, d2, d3

    def scatterData(self, m1, m2, key, func = lambda x: x):
        for d1, d2 in self.pair(m1, m2):
            if key is None:
                yield func(d1), func(d2)
            else:
                yield func(d1[key]), func(d2[key])

    def writeScatterData(self, fout, m1, m2, key, func = lambda x: x):
        m = [1000000, -1000000, 1000000, -1000000]
        for l1, l2 in self.scatterData(m1, m2, key, func):
            m[0] = min(m[0], l1)
            m[1] = max(m[1], l1)
            m[2] = min(m[2], l2)
            m[3] = max(m[3], l2)
            fout.write('{0} {1}\n'.format(l1, l2))

        return m

    def genScatterPlots(self, mtype, prefix, tpl, key, func = lambda x: x):
        for m1, m2 in itertools.combinations(mtype, 2):
            fn = prefix + '_scatter_{0}_{1}'.format(m1, m2)
            outfn = 'data/' + fn + '.data'
            fout = open(outfn, 'w')
            fout.write('# {0} {1}\n'.format(m1, m2))
            mx = self.writeScatterData(fout, m1, m2, key, func)
            fout.close()

            gnuplot = tpl.format(plotName(m1), plotName(m2), m1, m2)
            open('data/' + fn + '.gnuplot'.format(m1, m2), 'w').write(gnuplot)
            os.system('cd data && gnuplot {0}.gnuplot'.format(fn))
            print(prefix, m1, m2, mx)

    def genScatterM2(self):
        mtype = ['fd', 'fd:extend', 'h2', 'h2:extend', 'fa', 'fa:extend',
                 'rfa', 'rfa:extend']
        self.genScatterPlots(mtype, 'm2', gnuplot_scatter_m2,
                             'mutex2', lambda x: max(len(x), 0.1))

    def genScatterM(self):
        mtype = ['fd', 'fa', 'rfa']
        self.genScatterPlots(mtype, 'm', gnuplot_scatter_m,
                             'mutex', lambda x: max(len(x), 0.7))

    def genScatterVar(self):
        mtype = ['fd', 'fa', 'rfa']
        self.genScatterPlots(mtype, 'var', gnuplot_scatter_var, 'num-vars')

    def genScatterM2Time(self):
        mtype = ['fd', 'fd:extend', 'h2', 'h2:extend', 'fa', 'fa:extend',
                 'rfa', 'rfa:extend']
        self.genScatterPlots(mtype, 'm2_time', gnuplot_scatter_m2_time,
                             'mutex-time', lambda x: max(x, 0.01))

    def genScatterVarTime(self):
        mtype = ['fd', 'fa', 'rfa']
        self.genScatterPlots(mtype, 'var_time', gnuplot_scatter_var_time,
                             None, lambda x: max(x['time1'] + x['time2'] + x['mutex-time'], 0.01))

    def genScatterNumVars(self):
        mtype = ['fd', 'h2', 'fa', 'rfa', 'rfa-ilp', 'rfa-ilp-c']
        mtype += [x + ':extend' for x in mtype]
        self.genScatterPlots(mtype, 'vars', gnuplot_scatter_num_vars,
                             'num-vars')

    def genTableM2(self):
        mtype = ['fd', 'h2', 'fa', 'rfa']
        #mtype += [x + ':extend' for x in mtype]
        fout = open('data/m2_table.tex', 'w')
        fout.write('{\n')
        fout.write(r'\setlength{\tabcolsep}{0pt}' + '\n')
        fout.write(r'\begin{tabular}{l|c|' \
                        + '|'.join(['rl' for x in mtype]) + '}' + '\n')
        fout.write(r' \;\;\textbf{domain}\;\; & \;\;\textbf{\#ps}\;\; & ' \
                    + ' & '.join([r'\textbf{' + texName(x) + \
                    '} & \\textbf{+' + texName(x + ':extend') + r'}\;\;' for x in mtype]) \
                    + ' \\\\\n')
        fout.write('\\hline\n')

        s = { x : 0 for x in mtype }
        s2 = { x : 0 for x in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(r'\;\;' + dom + r'\;\;')
            fout.write(' & \;\;{0}\;\;'.format(len(self.data[mtype[0]][dom].values())))
            ps += len(self.data[mtype[0]][dom].values())
            for m in mtype:
                d = sum([len(x['mutex2']) for x in self.data[m][dom].values()])
                d2 = sum([len(x['mutex2']) for x in self.data[m + ':extend'][dom].values()])
                s[m] += d
                s2[m] += d2 - d
                fout.write(' & \\;\\;\\num{{{0}}} & +\\num{{{1}}}\\;\\;'.format(d, d2 - d))
            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'\;\;$\Sigma$\;\; & \;\;{0}\;\;'.format(ps))
        for m in mtype:
            fout.write(' & \\;\\;\\num{{{0}}} & +\\num{{{1}}}\\;\\;'.format(s[m], s2[m]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableM2Simple(self):
        mtype1 = ['fd', 'h2', 'fa', 'rfa']
        mtype2 = [x + ':extend' for x in mtype1]
        mtype = mtype1 + mtype2
        fn = 'm2sE'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|r|')
        fout.write('|'.join(['r' for x in mtype1]) + '|')
        fout.write('|'.join([r'r@{+}l' for x in mtype2]) + '}\n')
        fout.write(r'\textbf{domain} & \multicolumn{1}{c|}{\textbf{\#ps}} &' \
                    + ' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype1]) \
                    + ' & ' + ' & '.join([r'\multicolumn{2}{c|}{\textbf{' + texName(x) + '}}' for x in mtype2[:-1]]) \
                    + r' & \multicolumn{2}{c}{\textbf{' + texName(mtype2[-1]) + '}}'
                    + ' \\\\\n')
        fout.write('\\hline\n')

        s = { x : 0 for x in mtype }
        s2 = { x : 0 for x in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(dom)
            fout.write(' & {0}'.format(len(self.data[mtype[0]][dom].values())))
            ps += len(self.data[mtype[0]][dom].values())

            line = { m : sum([len(x['mutex2']) for x in self.data[m][dom].values()]) \
                        for m in mtype }
            maxline = max(line.values())

            for m in mtype:
                d2 = 0
                d = line[m]
                s[m] += d

                if m in mtype2:
                    m2, _ = m.split(':')
                    d2 = line[m2]
                    d2 = d - d2
                    s2[m] += d2

                ismax = False
                if d == maxline:
                    if m in mtype1:
                        ismax = True
                    elif d2 != 0:
                        ismax = True

                fout.write(' & ')
                if ismax:
                    fout.write(r'{\bfseries ')
                fout.write('\\num{{{0}}}'.format(d))
                if ismax:
                    fout.write(r'}')

                if m in mtype2:
                    fout.write(' (&\\num{{{0}}})'.format(d2))

            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'$\Sigma$ & {0}'.format(ps))
        for m in mtype:
            if m in mtype2:
                fout.write(' & \\num{{{0}}} (&\\num{{{1}}})'.format(s[m], s2[m]))
            else:
                fout.write(' & \\num{{{0}}}'.format(s[m]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableM2FullSimple(self):
        mtype1 = ['fd', 'h2', 'fa', 'rfa']
        mtype2 = [x + ':extend' for x in mtype1]
        mtype = mtype1 + mtype2
        fn = 'm2sEFull'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|l|r|')
        fout.write('|'.join(['r' for x in mtype1]) + '|')
        fout.write('|'.join([r'r@{+}l' for x in mtype2]) + '}\n')
        fout.write(r'\textbf{domain} & \textbf{problem} & \multicolumn{1}{c|}{\textbf{all}} &' \
                    + ' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype1]) \
                    + ' & ' + ' & '.join([r'\multicolumn{2}{c|}{\textbf{' + texName(x) + '}}' for x in mtype2[:-1]]) \
                    + r' & \multicolumn{2}{c}{\textbf{' + texName(mtype2[-1]) + '}}'
                    + ' \\\\\n')
        fout.write('\\hline\n')

        for domain, problem, mutex, unreach in sorted(self.full, key = lambda x: x[0]):
            prob = problem
            if domain == 'maintenance':
                prob = problem[12:]

            line = { m : len(self.data[m][domain][problem]['mutex2']) \
                        for m in mtype }
            maxline = max(line.values())

            fout.write('{0} & {1} & '.format(domain, prob))
            if len(mutex) == maxline:
                fout.write(r'{\bfseries ')
            fout.write('\\num{{{0}}}'.format(len(mutex)))
            if len(mutex) == maxline:
                fout.write(r'}')

            for m in mtype:
                d2 = 0
                d = line[m]
                if m in mtype2:
                    m2, _ = m.split(':')
                    d2 = line[m2]
                    d2 = d - d2

                ismax = False
                if d == maxline:
                    if m in mtype1:
                        ismax = True
                    elif d2 != 0:
                        ismax = True

                fout.write(' & ')
                if ismax:
                    fout.write(r'{\bfseries ')
                fout.write('\\num{{{0}}}'.format(d))
                if ismax:
                    fout.write(r'}')

                if m in mtype2:
                    fout.write(' (&\\num{{{0}}})'.format(d2))

            fout.write('\\\\\n')
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableM2Rate(self):
        mtype1 = ['fd', 'h2', 'fa', 'rfa']
        mtype2 = [x + ':extend' for x in ['fd', 'fa', 'rfa']]
        mtype = mtype1 + mtype2
        fn = 'm2sERate'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|')
        fout.write('|'.join(['r' for x in mtype1]) + '|')
        fout.write('|'.join([r'r' for x in mtype2]) + '}\n')
        fout.write(r'\textbf{domain} &' \
                    + ' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype1]) \
                    + ' & ' + ' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype2[:-1]]) \
                    + r' & \multicolumn{1}{c}{\textbf{' + texName(mtype2[-1]) + '}}'
                    + ' \\\\\n')
        fout.write('\\hline\n')

        s = { x : [] for x in mtype }
        s2 = { x : [] for x in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(dom)
            ps += len(self.data[mtype[0]][dom].values())

            line1 = { m : sum([len(x['mutex2']) for x in self.data[m][dom].values()]) \
                        for m in mtype }
            maxline = max(line1.values())
            line = { k : float(v) / maxline for k, v in line1.items() }

            for m in mtype:
                d2 = 0
                d = line[m]
                s[m] += [d]
                s2[m] += [line1[m]]

                fout.write(' & ')
                fout.write('\\num{{{0:.2f}}}'.format(d))

            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'Mean')
        for m in mtype:
            avg = numpy.mean(s[m])
            fout.write(' & \\num{{{0:.2f}}}'.format(avg))
        fout.write('\\\\\n')
#        fout.write(r'Overall')
#        for m in mtype:
#            avg = float(sum(s2[m])) / float(sum(s2['h2']))
#            fout.write(' & \\num{{{0:.2f}}}'.format(avg))
#        fout.write('\\\\\n')
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()


    def genTableTime(self):
        mtype = ['fd', 'h2', 'fa', 'rfa']
        #mtype += [x + ':extend' for x in mtype]
        fout = open('data/time_table.tex', 'w')
        fout.write('{\n')
        fout.write(r'\setlength{\tabcolsep}{0pt}' + '\n')
        fout.write(r'\begin{tabular}{l|c|' \
                        + '|'.join(['rl' for x in mtype]) + '}' + '\n')
        fout.write(r' \;\;\textbf{domain}\;\; & \;\;\textbf{\#ps}\;\; & ' \
                    + ' & '.join([r'\textbf{' + texName(x) + \
                    '} & \\textbf{+' + texName(x + ':extend') + r'}\;\;' for x in mtype]) \
                    + ' \\\\\n')
        fout.write('\\hline\n')

        s = { x : 0. for x in mtype }
        s2 = { x : 0. for x in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(r'\;\;' + dom + r'\;\;')
            fout.write(' & \;\;{0}\;\;'.format(len(self.data[mtype[0]][dom].values())))
            ps += len(self.data[mtype[0]][dom].values())
            for m in mtype:
                d = sum([x['mutex-time'] for x in self.data[m][dom].values()])
                d2 = sum([x['mutex-time'] for x in self.data[m + ':extend'][dom].values()])
                s[m] += d
                s2[m] += d2 - d
                fout.write(' & \\;\\;\\num{{{0:.2f}}} & +\\num{{{1:.2f}}}\\;\\;'.format(d, d2 - d))
            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'\;\;$\Sigma$\;\; & \;\;{0}\;\;'.format(ps))
        for m in mtype:
            fout.write(' & \\;\\;\\num{{{0:.2f}}} & +\\num{{{1:.2f}}}\\;\\;'.format(s[m], s2[m]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableTimeSimple(self):
        mtype1 = ['fd', 'h2', 'fa', 'rfa']
        mtype2 = [x + ':extend' for x in mtype1]
        mtype = mtype1 + mtype2
        fn = 'timesE'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|r|')
        fout.write('|'.join(['r' for x in mtype1]) + '|')
        fout.write('|'.join([r'r@{+}l' for x in mtype2]) + '}\n')
        fout.write(r'\textbf{domain} & \multicolumn{1}{c|}{\textbf{\#ps}} &' \
                    + ' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype1]) \
                    + ' & ' + ' & '.join([r'\multicolumn{2}{c|}{\textbf{' + texName(x) + '}}' for x in mtype2[:-1]]) \
                    + r' & \multicolumn{2}{c}{\textbf{' + texName(mtype2[-1]) + '}}'
                    + ' \\\\\n')
        fout.write('\\hline\n')

        s = { x : 0. for x in mtype }
        s2 = { x : 0. for x in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(dom)
            fout.write(' & {0}'.format(len(self.data[mtype[0]][dom].values())))

            line = { m : sum([x['mutex-time'] for x in self.data[m][dom].values()]) \
                        for m in mtype }
            min1, min2 = sorted(line.items(), key = lambda x: x[1])[0:2]

            ps += len(self.data[mtype[0]][dom].values())
            print(dom, [x['num-facts'] for x in self.data[mtype[0]][dom].values()], sum([x['num-facts'] for x in self.data[mtype[0]][dom].values()]))
            print('\t', [len(x['mutex2']) for x in self.data['h2'][dom].values()])
            for m in mtype:
                d2 = 0
                d = line[m]
                s[m] += d

                if m in mtype2:
                    m2, _ = m.split(':')
                    d2 = sum([x['mutex-time'] for x in self.data[m2][dom].values()])
                    d2 = d - d2
                    s2[m] += d2

                fout.write(' & ')
                if m == min1[0]:
                    fout.write(r'{\bfseries')

                fout.write('\\num{{{0:.2f}}}'.format(d))

                if m == min1[0]:
                    fout.write(r'}')

                if m in mtype2:
                    fout.write(' (&\\num{{{0:.2f}}})'.format(d2))

            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'$\Sigma$ & {0}'.format(ps))
        for m in mtype:
            if m in mtype2:
                fout.write(' & \\num{{{0:.2f}}} (&\\num{{{1:.2f}}})'.format(s[m], s2[m]))
            else:
                fout.write(' & \\num{{{0:.2f}}}'.format(s[m]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableTimeFullSimple(self):
        mtype1 = ['fd', 'h2', 'fa', 'rfa']
        mtype2 = [x + ':extend' for x in mtype1]
        mtype = mtype1 + mtype2
        fn = 'timesEFull'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|l|r|')
        fout.write('|'.join(['r' for x in mtype1]) + '|')
        fout.write('|'.join([r'r@{+}l' for x in mtype2]) + '}\n')
        fout.write(r'\textbf{domain} & \textbf{problem} & \multicolumn{1}{c|}{\textbf{all}} &' \
                    + ' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype1]) \
                    + ' & ' + ' & '.join([r'\multicolumn{2}{c|}{\textbf{' + texName(x) + '}}' for x in mtype2[:-1]]) \
                    + r' & \multicolumn{2}{c}{\textbf{' + texName(mtype2[-1]) + '}}'
                    + ' \\\\\n')
        fout.write('\\hline\n')

        for domain, problem, mutex, unreach in sorted(self.full, key = lambda x: x[0]):
            prob = problem
            if domain == 'maintenance':
                prob = problem[12:]
            fout.write('{0} & {1} & \\num{{{2}}}'.format(domain, prob, len(mutex)))
            for m in mtype:
                d = self.data[m][domain][problem]['mutex-time']
                if m in mtype2:
                    m2, _ = m.split(':')
                    d2 = self.data[m2][domain][problem]['mutex-time']
                    d2 = d - d2
                    fout.write(' & \\num{{{0:.2f}}} (&\\num{{{1:.2f}}})'.format(d, d2))
                else:
                    fout.write(' & \\num{{{0:.2f}}}'.format(d))
            fout.write('\\\\\n')
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableTimeMinMax(self):
        mtype1 = ['fd', 'h2', 'fa', 'rfa']
        mtype2 = [x + ':extend' for x in mtype1]
        mtype = mtype1 + mtype2
        fn = 'time_min_max'

        #mtype += [x + ':extend' for x in mtype]
        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        #fout.write(r'\setlength{\tabcolsep}{0pt}' + '\n')
        fout.write(r'\begin{tabular}{l|' \
                        + '|'.join(['rr' for x in mtype]) + '}' + '\n')
        fout.write(r'\multirow{2}{*}{\textbf{domain}}')
        for x in mtype[:-1]:
            fout.write(r' & \multicolumn{2}{c|}{\textbf{' + texName(x) + '}}')
        fout.write(r' & \multicolumn{2}{c}{\textbf{' + texName(mtype[-1]) + '}}')
        fout.write(r'\\' + '\n')
        fout.write(' & ' + ' & '.join([r'{\textbf{min}} & {\textbf{max}}' for x in mtype]))
        fout.write(r'\\' + '\n')
        fout.write('\\hline\n')

        smin = { x : 10000000. for x in mtype }
        smax = { x : 0. for x in mtype }
        s = { x : [] for x in mtype }
        for dom in data.domains():
            fout.write(dom)
            for m in mtype:
                d = [x['mutex-time'] for x in self.data[m][dom].values()]
                smin[m] = min(smin[m], min(d))
                smax[m] = max(smax[m], max(d))
                s[m] += d
                fout.write(' & {0:.2f} & {1:.2f}'.format(min(d), max(d)))
            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'Overall')
        for m in mtype:
            fout.write(' & {0:.2f} & {1:.2f} '.format(smin[m], smax[m]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def _genTableTimeMinMax(self, mtype, fn):
        #mtype += [x + ':extend' for x in mtype]
        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        #fout.write(r'\setlength{\tabcolsep}{0pt}' + '\n')
        fout.write(r'\begin{tabular}{l|c|' \
                        + '|'.join(['SSS' for x in mtype]) + '}' + '\n')
        fout.write(r'\multirow{2}{*}{\textbf{domain}} & \multirow{2}{*}{\textbf{\#ps}}')
        for x in mtype[:-1]:
            fout.write(r' & \multicolumn{3}{c|}{' + texName(x) + '}')
        fout.write(r' & \multicolumn{3}{c}{' + texName(mtype[-1]) + '}')
        fout.write(r'\\' + '\n')
        fout.write(' & &' + ' & '.join([r'{\textbf{min}} & {\textbf{max}} & {\textbf{gmean}}' for x in mtype]))
        fout.write(r'\\' + '\n')
        fout.write('\\hline\n')

        smin = { x : 10000000. for x in mtype }
        smax = { x : 0. for x in mtype }
        s = { x : [] for x in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(dom)
            fout.write(' & {0}'.format(len(self.data[mtype[0]][dom].values())))
            ps += len(self.data[mtype[0]][dom].values())
            for m in mtype:
                d = [x['mutex-time'] for x in self.data[m][dom].values()]
                smin[m] = min(smin[m], min(d))
                smax[m] = max(smax[m], max(d))
                s[m] += d
                avg = scipy.stats.mstats.gmean(d)
                avg = '{0:.2f}'.format(avg)
                fout.write(' & {0:.2f} & {1:.2f} & {2}' \
                            .format(min(d), max(d), avg))
            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'Overall & {0}'.format(ps))
        for m in mtype:
            avg = scipy.stats.mstats.gmean(s[m])
            fout.write(' & {0:.2f} & {1:.2f} & {2:.2f} '.format(smin[m], smax[m], avg))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableTime2(self):
        mtype = ['fd', 'h2', 'fa', 'rfa']
        self._genTableTimeMinMax(mtype, 'time2')
        mtype = [x + ':extend' for x in mtype]
        self._genTableTimeMinMax(mtype, 'time2e')

    def _genTableTimePerMutex(self, mtype, fn):
        #mtype += [x + ':extend' for x in mtype]
        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        #fout.write(r'\setlength{\tabcolsep}{0pt}' + '\n')
        fout.write(r'\begin{tabular}{l|' \
                        + '|'.join(['S' for x in mtype]) + '}' + '\n')
        fout.write(r'\textbf{domain}')
        for x in mtype:
            fout.write(r' & {\textbf{' + texName(x) + '}}')
        fout.write(r'\\' + '\n')
        fout.write('\\hline\n')

        sd = {m : 0. for m in mtype }
        sl = {m : 0 for m in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(dom)
            ps += len(self.data[mtype[0]][dom].values())
            for m in mtype:
                d = [x['mutex-time'] for x in self.data[m][dom].values()]
                mlen = sum([len(x['mutex2']) for x in self.data[m][dom].values()])
                if mlen > 0:
                    avg = sum(d) / mlen
                    avg *= 1000000
                    avg = '{0:.2f}'.format(avg)
                    sd[m] += sum(d)
                    sl[m] += mlen
                else:
                    avg = r'{\textemdash}'
                fout.write(' & {0}'.format(avg))
            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'Overall')
        for m in mtype:
            avg = sd[m] / sl[m]
            avg *= 1000000
            fout.write(' & {0:.2f} '.format(avg))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableTime3(self):
        mtype = ['fd', 'h2', 'fa', 'rfa']
        fn = 'time3'
        self._genTableTimePerMutex(mtype, fn)

        mtype = [x + ':extend' for x in mtype]
        fn = 'time3e'
        self._genTableTimePerMutex(mtype, fn)

    def genTableM2Subset(self):
        mtype = ['fd', 'h2', 'fa', 'rfa']
        mtype += [x + ':extend' for x in mtype]
        s = {}
#        for dom in self.domains():
#            d = {}
#            for m1 in mtype:
#                for m2 in mtype:
#                    if m1 == m2:
#                        continue
#                    if m1 not in d:
#                        d[m1] = {}
#                    if m2 not in d[m1]:
#                        d[m1][m2] = 0
#                    if m1 not in s:
#                        s[m1] = {}
#                    if m2 not in s[m1]:
#                        s[m1][m2] = 0
#
#                    for ds in self.tupleDom(dom, mtype):
#                        d[m1][m2] += len(set(ds[m1]['mutex2']) - set(ds[m2]['mutex2']))
#                        s[m1][m2] += len(set(ds[m1]['mutex2']) - set(ds[m2]['mutex2']))
#            print(dom)
#            pprint(d)

        x = 0
        y12 = 0
        y13 = 0
        y23 = 0
        for dom in self.domains():
            for ds in self.tupleDom(dom, mtype):
                x1 = set(ds['fa:extend']['mutex2']) - set(ds['fa']['mutex2'])
                x2 = set(ds['rfa:extend']['mutex2']) - set(ds['rfa']['mutex2'])
                x3 = set(ds['fd:extend']['mutex2']) - set(ds['fd']['mutex2'])
                x += len(x1 & x2 & x3)
                y12 += len(x1 & x2)
                y13 += len(x1 & x3)
                y23 += len(x2 & x3)

        pprint(s)
        print('X', x)
        print('y12', y12)
        print('y13', y13)
        print('y23', y23)

    def genTableM2Full(self):
        mtype = ['fd', 'h2', 'fa', 'rfa']
        #mtype += [x + ':extend' for x in mtype]
        fout = open('data/m2_full_table.tex', 'w')
        fout.write('{\n')
        fout.write(r'\setlength{\tabcolsep}{0pt}' + '\n')
        fout.write(r'\begin{tabular}{l|l|c|' \
                        + '|'.join(['rl' for x in mtype]) + '}' + '\n')
        fout.write(r' \;\;\textbf{domain}\;\; & \;\;\textbf{problem}\;\; & \;\;\textbf{all}\;\; & ' \
                    + ' & '.join([r'\textbf{' + texName(x) + \
                    '} & \\textbf{+' + texName(x + ':extend') + r'}\;\;' for x in mtype]) \
                    + ' \\\\\n')
        fout.write('\\hline\n')

        for domain, problem, mutex, unreach in sorted(self.full, key = lambda x: x[0]):
            prob = problem
            if domain == 'maintenance':
                prob = problem[12:]
            fout.write('\;\;{0}\;\; & \;\;{1}\;\; & \;\;\\num{{{2}}}\;\;'.format(domain, prob, len(mutex)))
            for m in mtype:
                d1 = len(self.data[m][domain][problem]['mutex2'])
                d2 = len(self.data[m + ':extend'][domain][problem]['mutex2'])
                d2 = d2 - d1
                fout.write(' & \;\;\\num{{{0}}} & +\\num{{{1}}}\;\;'.format(d1, d2))
            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def _mDominance(self, dom, m1, m2):
        sub_ps = 0
        for prob in self.data[m1][dom].keys():
            d1 = self.data[m1][dom][prob]
            d2 = self.data[m2][dom][prob]
            if len(d1['mutex']) < len(d2['mutex']):
                sub_ps += 1
                continue

            elif len(d1) == len(d2):
                mut1 = [self.mutexes[x] for x in d1['mutex']]
                mut2 = [self.mutexes[x] for x in d2['mutex']]
                add_ps = 0
                for mx1 in mut1:
                    for mx2 in mut2:
                        if mx1.issubset(mx2) and not mx2.issubset(mx1):
                            add_ps = 1
                            break
                    if add_ps == 1:
                        sub_ps += 1
                        break

        return sub_ps

    def genTableM(self):
        mtype = ['fd', 'fa', 'rfa']
        comb = [('fd', 'fa'), ('rfa', 'fa'), ('fd', 'rfa'), ('rfa', 'fd')]
        fn = 'm'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|r|')
        fout.write('|'.join(['r' for x in mtype]))
        fout.write('|')
        for x in comb:
            fout.write('|c')
        fout.write('}\n')
        fout.write(r'\textbf{domain} & \multicolumn{1}{c|}{\textbf{\#ps}} &')
        fout.write(' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype[:-1]]))
        fout.write(r' & \multicolumn{1}{c||}{\textbf{' + texName(mtype[-1]) + '}}')
        for c in comb:
            #fout.write(' & \\textbf{{{0}$\prec${1}}}'.format(*c))
            fout.write(' & \\textbf{{{1}$\succ${0}}}'.format(*c))
        fout.write(' \\\\\n')
        fout.write('\\hline\n')

        s = { x : 0 for x in mtype }
        sub = [0 for c in comb]
        ps = 0
        for dom in data.domains():
            fout.write(dom)
            fout.write(' & {0}'.format(len(self.data[mtype[0]][dom].values())))
            ps += len(self.data[mtype[0]][dom].values())

            line = { m : sum([len(x['mutex']) for x in self.data[m][dom].values()]) \
                        for m in mtype }
            maxline = max(line.values())

            for m in mtype:
                d = line[m]
                s[m] += d

                ismax = (d == maxline)

                fout.write(' & ')
                if ismax:
                    fout.write(r'{\bfseries ')
                fout.write('{0}'.format(d))
                if ismax:
                    fout.write(r'}')

            for i, c in enumerate(comb):
                x = self._mDominance(dom, c[0], c[1])
                fout.write(' & {0}'.format(x))
                sub[i] += x

            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'$\Sigma$ & {0}'.format(ps))
        for m in mtype:
            fout.write(' & {0}'.format(s[m]))
        for i, c in enumerate(comb):
            fout.write(' & {0}'.format(sub[i]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def _varDominance(self, dom, m1, m2):
        sub_ps = 0
        for prob in self.data[m1][dom].keys():
            d1 = self.data[m1][dom][prob]
            d2 = self.data[m2][dom][prob]
            if d1['num-vars'] > d2['num-vars']:
                sub_ps += 1

        return sub_ps

    def genTableVar(self):
        mtype = ['fd', 'fa', 'rfa']
        comb = [('fd', 'fa'), ('rfa', 'fa'), ('fd', 'rfa'), ('rfa', 'fd')]
        fn = 'var'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|r|')
        fout.write('|'.join(['r' for x in mtype]))
        fout.write('|')
        for x in comb:
            fout.write('|c')
        fout.write('}\n')
        fout.write(r'\textbf{domain} & \multicolumn{1}{c|}{\textbf{\#ps}} &')
        fout.write(' & '.join([r'\multicolumn{1}{c|}{\textbf{' + texName(x) + '}}' for x in mtype[:-1]]))
        fout.write(r' & \multicolumn{1}{c||}{\textbf{' + texName(mtype[-1]) + '}}')
        for c in comb:
            #fout.write(' & \\textbf{{{0}$\prec${1}}}'.format(*c))
            fout.write(' & \\textbf{{{1}$\succ${0}}}'.format(*c))
        fout.write(' \\\\\n')
        fout.write('\\hline\n')

        s = { x : 0 for x in mtype }
        sub = [0 for c in comb]
        ps = 0
        for dom in data.domains():
            fout.write(dom)
            fout.write(' & {0}'.format(len(self.data[mtype[0]][dom].values())))
            ps += len(self.data[mtype[0]][dom].values())

            line = { m : sum([x['num-vars'] for x in self.data[m][dom].values()]) \
                        for m in mtype }
            minline = min(line.values())

            for m in mtype:
                d = line[m]
                s[m] += d

                ismin = (d == minline)

                fout.write(' & ')
                if ismin:
                    fout.write(r'{\bfseries ')
                fout.write('{0}'.format(d))
                if ismin:
                    fout.write(r'}')

            for i, c in enumerate(comb):
                x = self._varDominance(dom, c[0], c[1])
                fout.write(' & {0}'.format(x))
                sub[i] += x

            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'$\Sigma$ & {0}'.format(ps))
        for m in mtype:
            fout.write(' & \\num{{{0}}}'.format(s[m]))
        for i, c in enumerate(comb):
            fout.write(' & {0}'.format(sub[i]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()

    def genTableVarTime(self):
        mtype = ['fd', 'fa', 'rfa']
        fn = 'var_time'

        fout = open('data/{0}_table.tex'.format(fn), 'w')
        fout.write('{\n')
        fout.write(r'\begin{tabular}{l|')
        fout.write('|'.join(['rrr' for x in mtype]) + '}\n')
        fout.write(r'\multirow{2}{*}{\textbf{domain}} &' \
                    + ' & '.join([r'\multicolumn{3}{c|}{\textbf{' + texName(x) + '}}' for x in mtype[:-1]]) \
                    + r' & \multicolumn{3}{c}{\textbf{' + texName(mtype[-1]) + '}}'
                    + ' \\\\\n')
        fout.write(' & ' + ' & '.join([r'{\textbf{sum}} & {\textbf{min}} & {\textbf{max}}' for x in mtype]))
        fout.write(r'\\' + '\n')
        fout.write('\\hline\n')

        s = { x : 0. for x in mtype }
        smin = { x : 100000. for x in mtype }
        smax = { x : 0. for x in mtype }
        ps = 0
        for dom in data.domains():
            fout.write(dom)

            line = { m : sum([x['time1'] + x['time2'] + x['mutex-time'] for x in self.data[m][dom].values()]) \
                        for m in mtype }
            lmin = { m : min([x['time1'] + x['time2'] + x['mutex-time'] for x in self.data[m][dom].values()]) \
                     for m in mtype }
            lmax = { m : max([x['time1'] + x['time2'] + x['mutex-time'] for x in self.data[m][dom].values()]) \
                        for m in mtype }
            min1, min2 = sorted(line.items(), key = lambda x: x[1])[0:2]

            ps += len(self.data[mtype[0]][dom].values())
            for m in mtype:
                d = line[m]
                s[m] += d
                smin[m] = min(smin[m], lmin[m])
                smax[m] = max(smax[m], lmax[m])


                fout.write(' & ')
                if m == min1[0]:
                    fout.write(r'{\bfseries')
                fout.write('{0:.2f}'.format(d))
                if m == min1[0]:
                    fout.write(r'}')

                fout.write(' & {0:.2f}'.format(lmin[m]))
                fout.write(' & {0:.2f}'.format(lmax[m]))


            fout.write('\\\\\n')
        fout.write('\\hline\n')
        fout.write(r'Overall')
        for m in mtype:
            fout.write(' & {0:.2f}'.format(s[m]))
            fout.write(' & {0:.2f}'.format(smin[m]))
            fout.write(' & {0:.2f}'.format(smax[m]))
        fout.write(r'\end{tabular}' + '\n')
        fout.write('}\n')
        fout.close()


data = Data()
data.load()

#data.genScatterM2()
#data.genScatterM2Time()
#data.genScatterNumVars()
#data.genTableM2()
#data.genTableM2Simple()
#data.genTableM2FullSimple()
#data.genTableM2Rate()
#data.genTableTimeSimple()
#data.genTableTimeFullSimple()
#data.genTableTimeMinMax()
#data.genTableTime()
#data.genTableTime2()
#data.genTableTime3()
#data.genTableM2Full()
#data.genTableM2Subset()
data.genTableM()
data.genTableVar()
data.genTableVarTime()
data.genScatterM()
data.genScatterVar()
data.genScatterVarTime()
