# coding=utf-8
'''
Created on 2018年12月6日

@author: robin huang(yuchonghuang@sina.cn)
'''
from RongZiRongQuan.RongZiRongQuan_SH import CRongZiRongQuan_SH
from TradingDays import getTradingDaysWithoutSperate, getTradingDaysWithSperate
from Configuration import RongZiRongQuan_DefaultFolder
from RongZiRongQuan.RongZiRongQuan_SZ import CRongZiRongQuan_SZ


def GetAllRongZhiRongQuan(_from=None, _to=None, path=None):

    if path is None:
        path = RongZiRongQuan_DefaultFolder
    allDates_SH = getTradingDaysWithoutSperate(_from, _to)
    allDates_SZ = getTradingDaysWithSperate(_from, _to)
    if allDates_SH is None or len(allDates_SH) == 0:
        print 'date error!'
        return False

    if allDates_SZ is None or len(allDates_SZ) == 0:
        print 'date error 1!'
        return False

    folder_SH = u'%s/沪市/' % (path)
    folder_SZ = u'%s/深市/' % (path)
    sh = CRongZiRongQuan_SH()
    sh.getRongZiRongQuanByDates(allDates_SH[:-1], folder_SH)

    sz = CRongZiRongQuan_SZ()
    sz.getRongZiRongQuanByDates(allDates_SZ[:-1], folder_SZ)


if __name__ == '__main__':
    folder = '/Volumes/Data/StockAssistant/StockData/RongZiRongQuan/'
    GetAllRongZhiRongQuan('2012-01-01', '2018-12-06', folder)
