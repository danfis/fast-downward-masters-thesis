#!/bin/bash
#/storage/praha1/home/danfis/dev/fd-full/full.sh /storage/praha1/home/danfis/dev/pddl-data/test-seq/depot/{domain,pfile1}.pddl

#python2 /storage/praha1/home/danfis/dev/fd-full/translate.py /storage/praha1/home/danfis/dev/pddl-data/test-seq/depot/{domain,pfile1}.pddl
python2 /storage/praha1/home/danfis/dev/fd-full/translate.py /storage/praha1/home/danfis/dev/pddl-data/ipc-2014/seq-opt/floortile/{domain,p01-4-3-2}.pddl
mv m.out /storage/praha1/home/danfis/metabench/full/floortile/
