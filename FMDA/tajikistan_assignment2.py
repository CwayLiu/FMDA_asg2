#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:18:04 2018

@author: cwayliu
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import csv
import tajikistan_assignment2_functions as fun

#%% task1
# read the data into python
file_name = 'tajikistan-TAVG-Trend.txt'
# create lists for data
(year, month, anomaly) = fun.readdata(file_name)
# calculate annual average
(annual_avg, yearList) = fun.calYearAvg(anomaly, year)
# print the average rate of temperature change
slope, intercept, r_value, p_value, std_err = stats.linregress(yearList, annual_avg)
print('the average rate of temperature change in °C / century is', slope * 100)

#%% task4
#  Plot the time series as well as the linear regression line into one figure
fun.plot_fig(yearList, annual_avg, intercept, slope)
