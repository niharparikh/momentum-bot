__author__ = 'Nihar'
__project__ = 'QuantAnalysis'

import talib
import os
import numpy as np

# DEFINE THRESHOLD FOR SUCCESS
success = 0.60

# HARD CODE PARAMETERS
right = 0.005
veryright = 0.015
delta = 30
upperbound = 80
lowerbound = 20

class Loader:

    def runtest(self, filename, success):

        # READ PRICES FILE
        close = np.loadtxt("dow30/" + filename, delimiter=',', skiprows=0, usecols=(5,))

        # READ ITERATION COLUMNS
        ind_duration = np.loadtxt('RSI_MA_Test.csv', delimiter=',', dtype='int', skiprows=1, usecols=(0,))
        metric_duration = np.loadtxt('RSI_MA_Test.csv', delimiter=',', dtype='int', skiprows=1, usecols=(1,))
        # delta = np.loadtxt('RSI_MA_Test.csv', delimiter=',', dtype='int', skiprows=1, usecols=(2,))
        # upperbound = np.loadtxt('RSI_MA_Test.csv', delimiter=',', dtype='int', skiprows=1, usecols=(3,))
        # lowerbound = np.loadtxt('RSI_MA_Test.csv', delimiter=',', dtype='int', skiprows=1, usecols=(4,))
        # right = np.loadtxt('RSI_MA_Test.csv', delimiter=',', skiprows=1, usecols=(5,))
        # veryright = np.loadtxt('RSI_MA_Test.csv', delimiter=',', skiprows=1, usecols=(6,))

        # PERFORM TESTS
        for i in range(len(ind_duration)):
            for l in range(len(metric_duration)):
                # for j in range(len(upperbound)):
                    # for k in range(len(right)):
                        percent1 = Loader().rsi_test(close, ind_duration[i], metric_duration[l], upperbound, lowerbound, right)
                        # percent1 = Loader().test(close, ind_duration[i], metric_duration[l], upperbound[j], lowerbound[j], right[k])
                        if (percent1 > success):
                            percent2 = Loader().rsi_test(close, ind_duration[i], metric_duration[l], upperbound, lowerbound, veryright)
                            # percent2 = Loader().test(close, ind_duration[i], metric_duration[l], upperbound[j], lowerbound[j], veryright[k])
                            percent3 = percent2 / percent1
                            print("\n{8}\nIndicator Duration: {0}, Metric Duration: {6}, OB/OS Delta: {1}, Right Delta: {2}, Very Right Delta: {3}\nRight Percentage: {4}, Very Right Percentage: {5}, Percentage of Very Right within Right: {7}".format(ind_duration[i], delta, right, veryright, percent1, percent2, metric_duration[l], percent3, filename))

    def rsi_test(self, p, id, md, ub, lb, r):

        # GENERATE METRIC
        ma = talib.MA(p, timeperiod=md)

        # GENERATE INDICATOR (RELATIVE STRENGTH INDEX)
        rsi = talib.RSI(p, timeperiod=id)

        # COMPARE RSI TO METRIC
        oversold = 0
        overbought = 0
        right = 0
        total = 0
        for i in range(id, len(rsi)):
            if (rsi[i] > ub):
                overbought += 1
                total += 1
                if (i < len(p)-md):
                    j = (1-r) * p[i]
                    if (ma[i+md] <= j):
                        right += 1
            if (rsi[i] < lb):
                oversold += 1
                total += 1
                if (i < len(p)-md):
                    j = (1+r) * p[i]
                    if (ma[i+md] >= j):
                        right += 1

        # CALCULATE STRENGTH OF INDICATOR
        percent = right / float(total)
        return percent

filecount = 0
for root, dirs, files in os.walk('dow30/'):
    for name in files:
        if (name == '.DS_Store'):
            continue
        Loader().runtest(name, success)
        filecount += 1
        print "\nFinished:", name