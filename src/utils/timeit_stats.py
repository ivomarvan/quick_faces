#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Mesure funtion call's time. Make statistics. 
'''


import time
import os
import sys

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.utils.common_containers import SortedContainer

class TimeStatisticItem:

    def __init__(self, name:str=''):
        self._count = 0
        self._sum = 0
        self._min = sys.float_info.max
        self._max = sys.float_info.min
        self._counOfNotEmpty = 0
        self._name = name

    def add(self, timeDif:float, result):
        self._sum += timeDif
        self._count += 1
        if timeDif > self._max:
            self._max = timeDif
        if timeDif < self._min:
            self._min = timeDif
        try:
            if result:
                self._counOfNotEmpty += 1
        except ValueError:
            if len(result):
                self._counOfNotEmpty += 1


    def getAvg(self, roundDigits:int=1):
        if self._count:
            return round(self._sum / self._count, roundDigits)

    def getCount(self):
        return self._count

    def getMin(self):
        return self._min

    def getMax(self):
        return self._max
    
    def getCounOfNotEmpty(self):
        return self._counOfNotEmpty

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

class TimeStatistics:

    data = {}

    @staticmethod
    def logTimeDiff(name, timeDiff, result):
        if name in TimeStatistics.data:
            timeStatItem = TimeStatistics.data[name]
        else:
            timeStatItem = TimeStatisticItem()
            TimeStatistics.data[name] = timeStatItem

        timeStatItem.add(timeDiff, result)

    @staticmethod
    def get_avg(name):
        try:
            timeStatItem = TimeStatistics.data[name]
            return  timeStatItem.getAvg()
        except KeyError:
            return 0

    @staticmethod
    def printStat():
        print('-'*80)
        print('Time statistics')
        print('-'*80)
        lengths = [len(s) for s in TimeStatistics.data.keys()]
        if len(lengths):
            maxLen = max(lengths)
        else:
            maxLen = 0
        for name, timeStatItem in TimeStatistics.data.items():
            printName = name + ' ' * (maxLen - len(name))
            total = timeStatItem.getCount()
            if total:
                successProcent = round(100 * timeStatItem.getCounOfNotEmpty() / timeStatItem.getCount(), 1)
                successProcent = str(successProcent) + ' %'

            else:
                successProcent = ''
            print('{}\tavg:{}\tmin:{}\tmax:{} [ms]\tsuccess:{}/{} ({})'.format(
                printName, timeStatItem.getAvg(),
                timeStatItem.getMin(), timeStatItem.getMax(),
                timeStatItem.getCounOfNotEmpty(),timeStatItem.getCount(), successProcent
        ))


    @staticmethod
    def print_tsv_header():
        print('\t'.join(['case', 'func', 'avg', 'min', 'max', 'count']))
        
    @staticmethod
    def print_as_tsv(case='', print_header:bool=True):
        # header
        if print_header:
            TimeStatistics.print_tsv_header()
        # sorted rows
        container = SortedContainer()
        for name, timeStatItem in TimeStatistics.data.items():
            timeStatItem.set_name(name)
            container.add(timeStatItem.getAvg(), timeStatItem)
        for timeStatItem in container.gen_sorted(reverse=True):
            print('\t'.join([str(x) for x in [case, timeStatItem.get_name(),  timeStatItem.getAvg(), timeStatItem.getMin(), timeStatItem.getMax(), timeStatItem.getCount()]]))


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        TimeStatistics.logTimeDiff(method.__name__, int((te - ts) * 1000), result)
        return result
    return timed
