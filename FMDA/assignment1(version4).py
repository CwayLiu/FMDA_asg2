#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 11:25:23 2018

@author: cwayliu
"""
import math
import matplotlib.pyplot as pl
import numpy as np
from scipy import stats

fin = open('tajikistan-TAVG-Trend.txt')

def toFloat(list):
    new_list = []
    for item in list:
        new_list.append(float(item))
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

#计算月际平均值
#list 数据数组
#m_list 月份数组
#year_range 年份长度
def calMonthInfo(list, m_list):
    averageList = []
    stdList = []
    rvsList = []
    for month in range(1, 12+1):
        subList = []
        for index in range(len(m_list)):
            if m_list[index] == str(month):
                subList.append(list[index])
        # 计算平均数
        mean = np.mean(subList)
        std = np.std(subList)
        rvs = stats.norm.rvs(loc=mean, scale=std, size=len(subList))

        averageList.append(mean)
        stdList.append(std)
        rvsList.append(rvs)

    return averageList, stdList, rvsList

(averageList, stdList, rvsList) = calMonthInfo(anomalyList, monthList)
month_std = np.std(averageList)
print(month_std)

#计算年际平均值
#list 数据数组
#y_list 年份数组
#year_from 起始年份
#year_to 结尾年份
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
print(year_std)

#task2

#计算概率密度
def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf

length = len(anomalyList)

frontList = anomalyList[0:int(length/2)]
backList = anomalyList[int(length/2):length]

#print(len(backList))

front_monthList = monthList[0:int(length/2)]
back_monthList = monthList[int(length/2):length]

front_yearList = yearList[0:int(length/2)]
back_yearList = yearList[int(length/2):length]

#mu, sigma = 0, 1
# x的范围为1951-2010，以0.001为单位,需x根据范围调试
x = np.arange(-5, 5, 0.001)
front_mean = np.mean(frontList)
front_std = np.std(frontList)
back_mean = np.mean(backList)
back_std = np.std(backList)

#print(front_mean, front_std, back_mean, back_std)

# x数对应的概率密度
front_y = normfun(x, front_mean, front_std)
back_y = normfun(x, back_mean, back_std)

# 参数,颜色，线宽
pl.plot(x, front_y, color = 'g', linewidth = 3)
pl.plot(x, back_y, color = 'b', linewidth = 3)

#数据，数组，颜色，颜色深浅，组宽，显示频率
pl.hist(frontList, bins = 12, color = 'r', alpha = 0.5, rwidth = 0.9, normed = True)
pl.hist(backList, bins = 12, color = 'y', alpha = 0.5, rwidth = 0.9, normed = True)
pl.show()
#pvalue=0?
print('前30年的pvalue：', stats.kstest(frontList, 'norm').pvalue)
print('后30年的pvalue：', stats.kstest(backList, 'norm').pvalue)

if stats.kstest(frontList, 'norm').pvalue < 0.05:
    print('前30年属于正态分布')

if stats.kstest(backList, 'norm').pvalue < 0.05:
    print('后30年属于正态分布')

#task3(?)
#计算前后三十年的月平均值
(front_averageList, front_stdList, front_rvsList) = calMonthInfo(frontList, front_monthList)
(back_averageList, back_stdList, back_rvsList) = calMonthInfo(backList, back_monthList)

front_year_averageList = calYearAvg(frontList, front_yearList, 1951, 1980)
back_year_averageList = calYearAvg(backList, back_yearList, 1981, 2010)

#平均值
month_diffList = []
for i in range(12):
    month_diffList.append(back_averageList[i] - front_averageList[i])
print(month_diffList)

year_diff = back_mean - front_mean
print(year_diff)
print(front_mean, back_mean)

front_rvs = stats.norm.rvs(loc=front_mean, scale=front_std, size=len(frontList))
back_rvs = stats.norm.rvs(loc=back_mean, scale=back_std, size=len(backList))
year_pvalue = stats.ttest_rel(front_rvs, front_rvs + back_rvs).pvalue
if(year_pvalue < 0.05):
    print('前后30年是正态分布，pvalue是', year_pvalue)

#标准差
month_diffList = []
month_ttestList = []
for i in range(12):
    month_diffList.append(back_stdList[i] - front_stdList[i])
    month_ttestList.append(stats.ttest_rel(front_rvsList[i], front_rvsList[i] + back_rvsList[i]).pvalue)
    if(month_ttestList[i] < 0.05):
        print(i + 1, '月是正态分布，pvalue是', month_ttestList[i])
    else:
        print(i + 1, '月不是正态分布，pvalue是', month_ttestList[i])
print('月差值：', month_diffList)
print('T检验：', month_ttestList)

#60年平均值kstest
month_std = np.std(averageList)
print(month_std)

print(stats.kstest(month_diffList, 'norm'))
#print(kstest(year_diffList, 'norm'))???

#绘制折线图
x = range(len(frontList))
y1 = [front_mean for i in range(360)]
y2 = [back_mean for i in range(360)]
pl.plot(x, frontList, color = 'g', linewidth = 1, linestyle = '-', label = 'front')
pl.plot(x, y1, color = 'g', linewidth = 1)
pl.plot(x, backList, color = 'b', linewidth = 1, linestyle = '-', label = 'back')
pl.plot(x, y2, color = 'b', linewidth = 1)
pl.legend(loc='upper left')
pl.ylabel('Tempreture')
pl.xlabel('Month')
pl.show()