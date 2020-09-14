'''
Created on Feb 18, 2020

@author: mizuno
'''
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import time

class Transition_lib2 :

    def __init__(self, df_ap, df_data, rank, size):
        self.df_ap = df_ap
        self.df_data = df_data
        self.aps = self.df_ap.AP.values.tolist()
        self.aps.append('out')
        self.transitions = [[0 for i in self.aps] for i in self.aps]
        self.transition_from = []
        self.transition_to = []
        self.duration = []
        self.clientid = []
        self.fromtime = []
        self.totime = []
        self.roop_index = 0
        self.duration_ap = []
        self.duration_n0 = [] 
        self.duration_ap_n0 = []
        self.each_duration = [0 for i in self.aps]
        self.each_duration_count = [0 for i in self.aps]
        self.rank = rank
        self.size = size
        print("Start this process for {0} of {1}".format(rank, size))

    def getCSV(self, file):
        return pd.read_csv(file, engine='python')

    def getDuplicate(self, df, column_name):
        return df.drop_duplicates(subset = column_name)

    def getTransition(self, df, df_unique):
        len_each = len(df_unique) / self.size 
        start = int(len_each * self.rank)
        end = int(len_each * (self.rank + 1))
        print("Start Number : {0}".format(start))
        print("End Number : {0}".format(end))

        pdf = pd.DataFrame(df)
        idx = start + 1
        #for i in df_unique['client'] :
        compute_time = 0
        for i in df_unique.iloc[start:end, 1]:
            #print(i)
            #print( str(idx) + '/' + str(len(df_unique)))
            idx += 1
            from_ap = self.aps.index('out')
            to_ap = -1
            start = time.time()
            for j in pdf.itertuples():
                if (j.client == i): 
                    for k in self.aps :
                        if (j.AP == k):
                            tmp_ap = self.aps.index(k) 
                            break
                    if(to_ap == -1 ): 
                        #print("First")
                        to_ap = tmp_ap
                        from_time = dt.datetime.strptime(j.timestamp, '%Y-%m-%d %H:%M:%S') 
                        #print(f"From_time : {from_time}")
                        to_time = dt.datetime.strptime(j.timestamp, '%Y-%m-%d %H:%M:%S')
                        #print(f"To_time : {to_time}")
                        #self.transition_from.append(self.aps.index('out'))
                        self.clientid.append(i)
                        self.transition_from.append(from_ap)
                        self.transition_to.append(to_ap)
                        self.duration.append(-1)
                        self.fromtime.append(from_time)
                        self.totime.append(to_time)
                        #self.duration_ap.append(self.aps.index('out'))
                        self.duration_ap.append(from_ap)
                    elif(to_ap >= 0) : 
                        if(to_ap == tmp_ap): 
                            #print("Continue")
                            to_time = dt.datetime.strptime(j.timestamp, '%Y-%m-%d %H:%M:%S')
                        else: 
                            #print("Different")
                            self.clientid.append(i)
                            self.transition_from.append(to_ap)
                            self.transition_to.append(tmp_ap)
                            to_time = dt.datetime.strptime(j.timestamp, '%Y-%m-%d %H:%M:%S')
                            delta = to_time - from_time
                            #print(delta)
                            #print(delta.total_seconds())
                            self.duration.append(delta.total_seconds())
                            self.fromtime.append(from_time)
                            self.totime.append(to_time)
                            self.duration_ap.append(to_ap)
                            from_ap = to_ap
                            to_ap = tmp_ap
                            from_time = dt.datetime.strptime(j.timestamp, '%Y-%m-%d %H:%M:%S')
                            #print(from_time)
                            #print(to_time)
            #print("Finish")
            self.clientid.append(i)
            self.transition_from.append(to_ap)
            self.transition_to.append(self.aps.index('out'))
            delta = to_time - from_time
            #print(delta)
            #if delta.total_seconds() < 10800 :
            self.duration.append(delta.total_seconds())
            self.fromtime.append(from_time)
            self.totime.append(to_time)
            #print(delta)
            #print(delta.total_seconds())
            elapsed_time = time.time() - start
            compute_time += elapsed_time
            #print ("Compute time for an unique MAC:{0}".format(elapsed_time) + "[sec]")

        compute_time = compute_time / len_each
        print ("Mean Compute time for an unique MAC:{0}".format(elapsed_time) + "[sec]")

        #print(self.transition_to)
        for i, j in zip(self.transition_from, self.transition_to):
            self.transitions[i][j] += 1
            #print(f"{i},{j}")
        #print(self.transition_from)
        #print(self.transition_to)
        return self.transitions


    def getDuration(self):
        sum = 0
        cnt = 0
        for i in self.duration:
            if(i > 0): 
                sum += i
                cnt += 1

        for i, j in zip(self.duration, self.duration_ap):
            if(i > 0 and i < 10800):
                self.duration_n0.append(i)
                self.duration_ap_n0.append(j)
                self.each_duration[j] += i
                self.each_duration_count[j] += 1

        idx = 0
        for i, j in zip(self.each_duration, self.each_duration_count):
            if( j > 0 ):
                self.each_duration[idx] = self.each_duration[idx] / self.each_duration_count[idx]
            idx += 1

        df = pd.DataFrame({'from':self.transition_from,'to':self.transition_to, 'duration':self.duration, 'clientid':self.clientid, 'from_time':self.fromtime,'to_time':self.totime})
        #df_n0 = pd.DataFrame({'from':self.transition_from_n0,'to':self.transition_to_n0, 'duration':self.duration_n0})
        #print(df_n0)
        #self.saveCSV(df, "./csv/duration"+str(self.rank)+".csv")
        #self.saveCSV(df_n0, './csv/durationall_n0_v2.csv')

        #print(self.duration_n0)
        #print(self.duration_ap_n0)
        #print(self.each_duration)
        #return sum / cnt
        return df

    def getEachDuration(self):
        return self.each_duration

    def saveCSV(self, df, fname):
        pdf = pd.DataFrame(df)
        pdf.to_csv(fname)
