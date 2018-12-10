# coding=utf-8
'''
Created on 2018-11-25 22:40:45
@author: robin huang(yuchonghuang@sina.cn)

'''
from PathUtility import IsFileExist
import pandas as pd


class CStrategyTestBase(object):
    def __init__(self):
        pass

    def Test(self, param1=None, param2=None, param3=None, param4=None):
        pass

    def _readStockHistoryInfoByID(self, stockID, folder=None):
        if folder is None:
            folder = u'../../../StockData/HistoryInfo/东方财富_后复权'

        fileName = u'%s/%s.csv' % (folder, stockID)
        if not IsFileExist(fileName):
            return None

        df = pd.read_csv(fileName)
        return df

    def _readIndexHitoryInfoByID(self, indexID, folder=None):
        if folder is None:
            folder = u'../../../StockData/HistoryInfo/东方财富_指数'

        fileName = u'%s/%s.csv' % (folder, indexID)
        if not IsFileExist(fileName):
            return None

        df = pd.read_csv(fileName)
        return df


if __name__ == '__main__':
    base = CStrategyTestBase()
    print base._readStockHistoryInfoByID('000008')
    print base._readIndexHitoryInfoByID('BK01541')
