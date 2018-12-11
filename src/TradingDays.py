# coding=utf-8
'''
Created on 2018年12月2日

@author: robin huang(yuchonghuang@sina.cn)
'''
import pandas as pd
import datetime


def is_holiday(date, file_='./calendar.csv'):
    '''
    判断是否为交易日，返回True or False
    '''
    df = pd.read_csv(file_)
    holiday = df[df.isOpen == 0]['calendarDate'].values
    if isinstance(date, str):
        today = datetime.datetime.strptime(date, '%Y-%m-%d')

    if today.isoweekday() in [6, 7] or str(date) in holiday:
        return True
    else:
        return False


def getTradingDays(_from=None, _to=None, file_='./calendar.csv'):
    df = pd.read_csv(file_)
    allTradingDays = df[df.isOpen == 1]['calendarDate']
    if _from is not None:
        allTradingDays = allTradingDays[allTradingDays >= _from]

    if _to is None:
        _to = str(datetime.date.today())

    allTradingDays = allTradingDays[allTradingDays <= _to]
    return allTradingDays


def getTradingDaysWithSperate(_from=None, _to=None):
    return getTradingDays(_from, _to).values


def getTradingDaysWithoutSperate(_from=None, _to=None):
    return getTradingDays(_from, _to).replace('-', '', regex=True).values


if __name__ == '__main__':
    #print datetime.date.today()
    print getTradingDaysWithoutSperate(_from='2017-05-13', _to=None)
