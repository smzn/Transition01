'''
Created on Feb 18, 2020

@author: mizuno
'''
import Transition_lib2 as mdl
import time
from mpi4py import MPI
import pandas as pd

def getCSV(file):
    return pd.read_csv(file, engine='python')

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start = time.time()
df_ap = getCSV('./csv/APlocations.csv')
#print(df_ap.head())
print("Number of AP : {0}".format(len(df_ap)))

df_data = getCSV('./csv/2014_09_uniq.csv')
#df_data = getCSV('./csv/test500000.csv')
#print(df_data.head())
print("Number of Data : {0}".format(len(df_data)))

elapsed_time = time.time() - start
print ("data_import_time:{0}".format(elapsed_time) + "[sec]")

tlib = mdl.Transition_lib2(df_ap, df_data, rank, size)

df_unique = tlib.getDuplicate(df_data, 'client')
print("Number of Unique Mac Address : {0}".format(len(df_unique)))

start = time.time()
#transitions = tlib.getTransition(df_data, df_unique)
transitions = tlib.getTransition(df_data, df_unique)
elapsed_time = time.time() - start
print ("Transition_Compute_time:{0}".format(elapsed_time) + "[sec]")
tlib.saveCSV(transitions, "./csv/2014_09_24/transitions"+str(rank)+".csv")

duration = tlib.getDuration()
#print(duration)
tlib.saveCSV(duration, "./csv/2014_09_24/duration"+str(rank)+".csv")

each_duration = tlib.getEachDuration()
#print(each_duration)

