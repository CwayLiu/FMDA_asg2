#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 23:38:35 2018

@author: cwayliu
"""
import matplotlib.pyplot as pl
import numpy as np
from scipy import stats
import csv
#read file
fin = open('tajikistan-TAVG-Trend.txt')

def toFloat(list):
    new_list = []
    for item in list:
        new_list.append(float(item))
    return new_list

def toString(list):
    new_list = []
    for item in list:
        new_list.append(str(item))
    return new_list

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

    anomalyList = toFloat(anomalyList)
#%%task1
print("the number of data records is", len(anomalyList))

count = 0
for line in fin:
    list_space = line.strip().split()
    for NaN in list_space:
        if NaN == 'NaN':
            count = count + 1
            break
print("the share of missing values is", str(count*100/len(anomalyList))+"%")

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
print("the share of ties is", str(100*(1-(count/len(anomalyList))))+"%")
#list create/devide
length = len(anomalyList)

frontList = anomalyList[0:int(length/2)]
backList = anomalyList[int(length/2):length]

front_monthList = monthList[0:int(length/2)]
back_monthList = monthList[int(length/2):length]

front_yearList = yearList[0:int(length/2)]
back_yearList = yearList[int(length/2):length]

#average of the anomaly in the reference period 
s = 0
for average in frontList:
    s = s + average
print("average of the anomaly in the reference period ", s/360)
print("average of the anomaly in the reference period is close to 0.")
#month average
#m_list month list
def calMonthInfo(list, m_list):
    averageList = []
    stdList = []
    rvsList = []
    for month in range(1, 12+1):
        subList = []
        for index in range(len(m_list)):
            if m_list[index] == str(month):
                subList.append(list[index])
        #average
        mean = np.mean(subList)
        std = np.std(subList)
        rvs = stats.norm.rvs(loc=mean, scale=std, size=len(subList))

        averageList.append(mean)
        stdList.append(std)
        rvsList.append(rvs)

    return averageList, stdList, rvsList

(averageList, stdList, rvsList) = calMonthInfo(anomalyList, monthList)
month_std = np.std(averageList)
print("intraannual variation:", month_std)

#year average
def calYearAvg(list, y_list, year_from, year_to):
    year_averageList = []
    for year in range(year_from, year_to+1):
        count = 0
        for index in range(len(y_list)):
            if y_list[index] == str(year):
                count = count + list[index]
        average = count/12
        year_averageList.append(average)
    return year_averageList

year_averageList = calYearAvg(anomalyList, yearList, 1951, 2010)
year_std = np.std(year_averageList)
print("interannual variation:", year_std)

#%%task2
#density
def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf
#0.001 as unit
x = np.arange(-5, 5, 0.001)
front_mean = np.mean(frontList)
front_std = np.std(frontList)
back_mean = np.mean(backList)
back_std = np.std(backList)

front_y = normfun(x, front_mean, front_std)
back_y = normfun(x, back_mean, back_std)
#plot histograms and curves and save
pl.title("Theretical normal distribution of 1951-1980")
pl.xlabel("Anomaly")
pl.ylabel("Density")
pl.plot(x, front_y, color = 'g', linewidth = 3)
pl.hist(frontList, bins = 12, color = 'r', alpha = 0.5, rwidth = 0.9, normed = True)
pl.savefig("tajikistan_1951-1980_series.png")
pl.show()

pl.title("Theretical normal distribution of 1981-2010")
pl.xlabel("Anomaly")
pl.ylabel("Density")
pl.plot(x, back_y, color = 'y', linewidth = 3)
pl.hist(backList, bins = 12, color = 'b', alpha = 0.5, rwidth = 0.9, normed = True)
pl.savefig("tajikistan_1981-2010_series.png")
pl.show()

pl.title("Theretical normal distribution of 1951-2010")
pl.xlabel("Anomaly")
pl.ylabel("Density")
pl.plot(x, front_y, color = 'g', linewidth = 3)
pl.plot(x, back_y, color = 'b', linewidth = 3)
pl.hist(frontList, bins = 12, color = 'r', alpha = 0.5, rwidth = 0.9, normed = True)
pl.hist(backList, bins = 12, color = 'y', alpha = 0.5, rwidth = 0.9, normed = True)
pl.savefig("tajikistan_1951-2010_series.png")
pl.show()

print('p-value of 1951-1980 is', stats.kstest(frontList, 'norm').pvalue)
print('p-value of 1981-2010 is', stats.kstest(backList, 'norm').pvalue)
#reason for choice (why choose non-parametric)
if stats.kstest(frontList, 'norm').pvalue < 0.05:
    print('period 1951-1980 is normally distributed(accept)')

if stats.kstest(backList, 'norm').pvalue < 0.05:
    print('period 1981-2010 is normally distributed(accept)')

#%%task3
#average calculation
(front_averageList, front_stdList, front_rvsList) = calMonthInfo(frontList, front_monthList)
(back_averageList, back_stdList, back_rvsList) = calMonthInfo(backList, back_monthList)

front_year_averageList = calYearAvg(frontList, front_yearList, 1951, 1980)
back_year_averageList = calYearAvg(backList, back_yearList, 1981, 2010)
#difference
month_diffList = []
for i in range(12):
    month_diffList.append(back_averageList[i] - front_averageList[i])
print('month difference:',month_diffList)

year_diff = back_mean - front_mean
print('year difference:',year_diff)
print(front_mean, back_mean)

front_rvs = stats.norm.rvs(loc=front_mean, scale=front_std, size=len(frontList))
back_rvs = stats.norm.rvs(loc=back_mean, scale=back_std, size=len(backList))
year_pvalue = stats.ttest_rel(front_rvs, front_rvs + back_rvs).pvalue
if(year_pvalue < 0.05):
    print('period 1951-1980 are normally distributed, and p-value is', year_pvalue)
#std and ttest
month_stdList = []
month_ttestList = []
for i in range(12):
    month_stdList.append(back_stdList[i] - front_stdList[i])
    month_ttestList.append(stats.ttest_rel(front_rvsList[i], front_rvsList[i] + back_rvsList[i]).pvalue)
    if(month_ttestList[i] < 0.05):
        print(i + 1, 'non-rejection of the null hypothesis, and p-value is', month_ttestList[i])
    else:
        print(i + 1, 'rejection of the null hypothesis, and p-value is', month_ttestList[i])
print('standard deviation of month:',month_stdList)
print('Ttest:', month_ttestList)

#output csv
csvfile = open('tajikistan_statistics.csv', 'w', newline='')
writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['time', 'difference in averages in celcius', 'standard deviation 1951-1980', 'standard deviation 1981-2010', 'p-value', 'interpretation of the p-value'])
writer.writerow(['year', year_diff, front_std, back_std, year_pvalue, bool(year_pvalue < 0.05)])
for i in range(12):
    row = []
    row.append(i+1)
    row.append(month_diffList[i])
    row.append(front_stdList[i])
    row.append(back_stdList[i])
    row.append(month_ttestList[i])
    row.append(bool(month_ttestList[i]))
    writer.writerow(row)
csvfile.close()
#plot
x = range(len(frontList))
y1 = [front_mean for i in range(360)]
y2 = [back_mean for i in range(360)]
pl.plot(x, frontList, color = 'g', linewidth = 1, linestyle = '-', label = '1951-1980')
pl.plot(x, y1, color = 'b', linewidth = 1, label = 'mean of 1951-1980')
pl.plot(x, backList, color = 'r', linewidth = 1, linestyle = '-', label = '1981-2010')
pl.plot(x, y2, color = 'm', linewidth = 1, label = 'mean of 1981-2010')
pl.legend(loc='upper left')
pl.title('Temperature difference compared to 1951-1980 average')
pl.ylabel('Temperature in celcius')
pl.xlabel('Time in Months')
pl.savefig("tajikistan_time_series.png")
pl.show()