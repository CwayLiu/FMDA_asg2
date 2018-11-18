#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 11:25:23 2018

@author: cwayliu
"""
import math
import matplotlib.pyplot as pl
import numpy as np

fin = open('tajikistan-TAVG-Trend.txt')

yearList = []
monthList = []
anomalyList = []

for line in fin:
    list_space = line.strip().split()
    if len(list_space)==0 or line.startswith('%'): continue
    year = list_space[0]
    month = list_space[1]
    anomaly = list_space[2] 
    
    if int(year) in range(1951, 2010+1): 
        yearList.append(year)
        monthList.append(month)
        anomalyList.append(anomaly)
#task1(a)
print("the number of data records is", len(anomalyList))
#task1(b)
count = 0
for line in fin:
    list_space = line.strip().split()
    for NaN in list_space:
        if NaN == 'NaN':
            count = count + 1
            break
print("the share of missing values is", str(count*100/len(anomalyList))+"%")
#task1(c)
dict = {}
for item in anomalyList:
    if item in dict:
        dict[item] = dict[item]
    else:
        dict[item] = 1
count = 0
for key, value in dict.items():
    if value == 1:
        count = count + 1
print(str(100*(1-(count/len(anomalyList))))+"%")
averageList = []
for month in range(1, 12+1):
    for index in range(len(monthList)):
        if monthList[index] == str(month):
            count = count + float(anomalyList[index])
    average = count/60
    averageList.append(average)
print(np.std(averageList))
year_averageList = []
for year in range(1951, 2010+1):
    for index in range(len(yearList)):
        if yearList[index] == str(year):
            count = count + float(anomalyList[index])
    average = count/12
    year_averageList.append(average)
print(np.std(year_averageList))
