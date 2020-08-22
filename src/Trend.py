__author__ = 'Nihar'
__project__ = 'QuantAnalysis'

import talib
import os
import numpy as np

# DEFINE THRESHOLD FOR SUCCESS
success = 75

# HARD CODE PARAMETERS
right = 0.03
veryright = 0.05
delta = 30
upperbound = 80
lowerbound = 20

class LongTerm:

    def analysis(self, filename):

        # READ PRICES FILE
        close = np.loadtxt("dow30/" + filename, delimiter=',', skiprows=0, usecols=(5,))
        date = np.loadtxt("dow30/" + filename, delimiter=',', dtype='int', skiprows=0, usecols=(0,))

        # READ ITERATION COLUMNS
        ind_duration = np.loadtxt('RSI_MA_LongTerm.csv', delimiter=',', dtype='int', skiprows=1, usecols=(0,))
        metric_wait = np.loadtxt('RSI_MA_LongTerm.csv', delimiter=',', dtype='int', skiprows=1, usecols=(1,))
        metric_duration = np.loadtxt('RSI_MA_LongTerm.csv', delimiter=',', dtype='int', skiprows=1, usecols=(2,))

        # PERFORM TESTS
        for i in range(len(ind_duration)):
            for l in range(len(metric_wait)):
                for j in range(len(metric_duration)):
                    # for k in range(len(right)):
                        percent1 = int((LongTerm().rsi_test(close, date, ind_duration[i], metric_wait[l], metric_duration[j], upperbound, lowerbound, right)) * 100)
                        if (percent1 > success):
                            percent2 = int(LongTerm().rsi_test(close, date, ind_duration[i], metric_wait[l], metric_duration[j], upperbound, lowerbound, veryright) * 100)
                            percent3 = int(percent2 * 100 / percent1)
                            print("\n{6}\nIndicator Duration: {0}, Metric Wait: {2}, Metric Duration: {1}\nRight Percentage: {3}, Very Right Percentage: {4}, Percentage of Very Right within Right: {5}\n".format(ind_duration[i], metric_duration[j], metric_wait[l], percent1, percent2, percent3, filename))
                        # else:
                            # print("Signal not significantly successful.")
    def rsi_test(self, p, d, id, mw, md, ub, lb, r):

        # GENERATE METRIC
        ma = talib.MA(p, timeperiod=md)

        # GENERATE INDICATOR (RELATIVE STRENGTH INDEX)
        rsi = talib.RSI(p, timeperiod=id)

        # COMPARE RSI TO METRIC
        oversold = 0
        overbought = 0
        buy = 0
        sell = 0
        right = 0
        total = 0
        for i in range(id, len(rsi)):
            if (rsi[i] > ub):
                overbought += 1
                total += 1
                if (i < len(p)-mw):
                    j = (1-r) * p[i]
                    if (ma[i+mw] <= j):
                        sell += 1
                        right += 1
                        # print str(right) + ' ' + str(d[i]) + " SELL"
            if (rsi[i] < lb):
                oversold += 1
                total += 1
                if (i < len(p)-mw):
                    j = (1+r) * p[i]
                    if (ma[i+mw] >= j):
                        buy += 1
                        right += 1
                        # print str(right) + ' ' + str(d[i]) + " BUY"

        # CALCULATE STRENGTH OF INDICATOR
        if (total >= 15):
            percent = right / float(total)
            # print "Good Buy:" + str(buy) + " Good Sell:" + str(sell) + " Total:" + str(total)
        else: percent = 0
        return percent

filecount = 0
for root, dirs, files in os.walk('dow30/'):
    for name in files:
        if (name == '.DS_Store'):
            continue
        LongTerm().analysis(name)
        filecount += 1
        print "\nFinished:", name