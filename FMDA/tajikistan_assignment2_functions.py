#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 12:14:05 2018

@author: cwayliu
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

#%% task1
# file read
def readdata(file_name):
    # open the file
    fin = open(file_name, 'r')
    # create lists for data
    year = []
    month = []
    anomaly = []
    # skip space and comments
    for line in fin:
        data = line.strip().split()
        if line.startswith('%') or len(data)==0:
            continue
        # subset them to start in 1960
        if int(data[0]) >= 1960:
            # devide into year, month, anomaly
            year.append(data[0])
            month.append(data[1])
            anomaly.append(data[2])
    return(year, month, anomaly)

# annual averages
def calYearAvg(anomalylist, yearlist):
    # create lists for averages and years
    annual_avg = []
    yearList = []
    # loop for calculate annual data
    for year in range(1961, 2012+1):
       sumlist = []
       for index in range(len(yearlist)):
           if yearlist[index] == str(year):
               sumlist.append(float(anomalylist[index]))
       # create a actual year list
       yearList.append(year)
       # use numpy to calculate and add to list
       annual_avg.append(np.mean(sumlist))
    return (annual_avg, yearList)

# plot figure
def plot_fig(x, y, intercept, slope):
    x=np.array(x)
    y=np.array(y)
    plt.plot(x, y, color = 'b', linewidth = 1, label = 'linear regression line')    
    plt.plot(x, intercept+slope*x, 'r', label='fitted line')
    plt.legend(loc = 'upper left')
    plt.title('Linear regression model')
    plt.ylabel('Annual average')
    plt.xlabel('Time in year')
    plt.savefig('tajikistan_time_series')
    plt.show()

# evaluate model: percent bias    
def pbias():