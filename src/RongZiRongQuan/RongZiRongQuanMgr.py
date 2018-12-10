# coding=utf-8
'''
Created on 2018年12月6日

@author: robin huang(yuchonghuang@sina.cn)
'''
from RongZiRongQuan.RongZiRongQuan_SH import CRongZiRongQuan_SH
from TradingDays import getTradingDaysWithoutSperate
from Configuration import RongZiRongQuan_DefaultFolder
from RongZiRongQuan.RongZiRongQuan_SZ import CRongZiRongQuan_SZ


def GetAllRongZhiRongQuan(_from=None, _to=None, path=None):

    if path is None:
        path = RongZiRongQuan_DefaultFolder
    allDates = getTradingDaysWithoutSperate(_from, _to)
    if allDates is None or len(allDates) == 0:
        print 'date error!'
        return False

    folder_SH = u'%s/沪市/' % (path)
    folder_SZ = u'%s/深市/' % (path)
    sh = CRongZiRongQuan_SH()
    sh.getRongZiRongQuanByDates(allDates, folder_SH)

    sz = CRongZiRongQuan_SZ()
    sz.getRongZiRongQuanByDates(allDates, folder_SZ)


if __name__ == '__main__':
    folder = '/Volumes/Data/StockAssistant/StockData/RongZiRongQuan/'
    GetAllRongZhiRongQuan('2012-01-01', '2018-12-06', folder)
