#!/bin/bash
#/storage/praha1/home/danfis/dev/fd-full/full.sh /storage/praha1/home/danfis/dev/pddl-data/test-seq/depot/{domain,pfile1}.pddl

#python2 /storage/praha1/home/danfis/dev/fd-full/translate.py /storage/praha1/home/danfis/dev/pddl-data/test-seq/depot/{domain,pfile1}.pddl
python2 /storage/praha1/home/danfis/dev/fd-full/translate.py /storage/praha1/home/danfis/dev/pddl-data/ipc-2014/seq-opt/hiking/{domain,ptesting-1-2-3}.pddl
mv m.out /storage/praha1/home/danfis/metabench/full/hiking/