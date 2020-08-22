__author__ = 'Nihar'
__project__ = 'QuantAnalysis'

import talib
import os
import numpy as np

# DEFINE THRESHOLD FOR SUCCESS
success = 75

# HARD CODE PARAMETERS
right = 0.03
veryright = 0.06
delta = 10
# upperbound = 70
# lowerbound = 30
ind_duration = 5
metric_wait = 15
metric_duration = 5
# percent = 0

class initialize:

    def __init__(self, filename):
        self.name = filename[6:-4]
        self.open = np.loadtxt("dow30/" + filename, delimiter=',', skiprows=0, usecols=(2,))
        self.high = np.loadtxt("dow30/" + filename, delimiter=',', skiprows=0, usecols=(3,))
        self.low = np.loadtxt("dow30/" + filename, delimiter=',', skiprows=0, usecols=(4,))
        self.close = np.loadtxt("dow30/" + filename, delimiter=',', skiprows=0, usecols=(5,))
        self.date = np.loadtxt("dow30/" + filename, delimiter=',', dtype='int', skiprows=0, usecols=(0,))
        self.total = 0
        self.sellright = 0
        self.buyright = 0
        self.right = 0

    def run(self):
        rsi_ub = initialize.rsi_ub_test(self)
        rsi_lb = initialize.rsi_lb_test(self)
        stoch_ub = initialize.stoch_ub_test(self)
        stoch_lb = initialize.stoch_lb_test(self)
        cci_ub = initialize.cci_ub_test(self)
        cci_lb = initialize.cci_lb_test(self)
        initialize.compare_ub(self, rsi_ub, stoch_ub, cci_ub)
        initialize.compare_lb(self, rsi_lb, stoch_lb, cci_lb)
        if(self.total > 0):
            percent = float(self.right) / self.total
            print("{0} Percent: {8}\n Delta: {5}, ID: {6}, MW: {7}\n Total: {1}, Right: {2}, Sell Right: {3}, Buy Right: {4}\n".format(self.name, self.total, self.right, self.sellright, self.buyright, delta, ind_duration, metric_wait, percent))

    def rsi_ub_test(self):
        rsi = talib.RSI(self.close, timeperiod=ind_duration)
        li = []
        for i in range(ind_duration, len(rsi)):
                if (rsi[i] > upperbound):
                    li.append(i)
        return li

    def rsi_lb_test(self):
        rsi = talib.RSI(self.close, timeperiod=ind_duration)
        li = []
        for i in range(ind_duration, len(rsi)):
                if (rsi[i] < lowerbound):
                    li.append(i)
        return li

    def stoch_ub_test(self):
        fastk, fastd = talib.STOCHRSI(self.close, timeperiod=ind_duration)
        li = []
        for i in range(ind_duration, len(fastd)):
                if (fastd[i] > upperbound):
                    li.append(i)
        return li

    def stoch_lb_test(self):
        fastk, fastd = talib.STOCHRSI(self.close, timeperiod=ind_duration)
        li = []
        for i in range(ind_duration, len(fastd)):
                if (fastd[i] < lowerbound):
                    li.append(i)
        return li

    def cci_ub_test(self):
        cci = talib.CCI(self.high, self.low, self.close, timeperiod=ind_duration)
        li = []
        for i in range(ind_duration, len(cci)):
                if (cci[i] > (upperbound + 120)):
                    li.append(i)
        return li

    def cci_lb_test(self):
        cci = talib.CCI(self.high, self.low, self.close, timeperiod=ind_duration)
        li = []
        for i in range(ind_duration, len(cci)):
                if (cci[i] < (lowerbound - 220)):
                    li.append(i)
        return li

    def compare_ub(self, rsi_ub, stoch_ub, cci_ub):
        ma = talib.MA(self.close, timeperiod=metric_duration)
        for i in range(len(rsi_ub)):
            for j in range(len(stoch_ub)):
                for k in range(len(cci_ub)):
                    if(rsi_ub[i] == stoch_ub[j] and rsi_ub[i] == cci_ub[k]):
                        self.total += 1
                        index = rsi_ub[i]
                        if (index < (len(self.close)-metric_wait)):
                            check = (1-veryright) * self.close[index]
                            if (ma[index+metric_wait] <= check):
                                self.sellright += 1
                                self.right += 1

    def compare_lb(self, rsi_lb, stoch_lb, cci_lb):
        ma = talib.MA(self.close, timeperiod=metric_duration)
        for i in range(len(rsi_lb)):
            for j in range(len(stoch_lb)):
                for k in range(len(cci_lb)):
                    if(rsi_lb[i] == stoch_lb[j] and rsi_lb[i] == cci_lb[k]):
                        self.total += 1
                        index = rsi_lb[i]
                        if (index < (len(self.close)-metric_wait)):
                            check = (1+veryright) * self.close[index]
                            if (ma[index+metric_wait] >= check):
                                self.buyright += 1
                                self.right += 1

filecount = 0
for root, dirs, files in os.walk('dow30/'):
    for name in files:
        # print 'Finished:', filecount, '/ 30'
        # if (name == '.DS_Store'):
        #     continue
        if (name != 'table_axp.csv'):
            continue
        for delta in xrange(delta, 40, 5):
            upperbound = 50 + delta
            lowerbound = 50 - delta
            for ind_duration in xrange(ind_duration, 20):
                for metric_wait in xrange(metric_wait, 65, 10):
                    x = initialize(name).run()
        filecount += 1
        # print "\nFinished:", name

