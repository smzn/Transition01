#!/bin/csh
#PBS -q OCTOPUS
#PBS -l elapstim_req=03:00:00,cpunum_job=24
#PBS -M mizuno.shinya@sist.ac.jp,ohba.haruka@sist.ac.jp
#PBS -m bea
#PBS -b 1
cd $PBS_O_WORKDIR
mpiexec -n 24 python3 Transition_main_201409_24_2.py > result2014_09_1_24_2.txt
