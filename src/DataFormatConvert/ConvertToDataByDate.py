# coding=utf-8
'''
Created on 2018-12-19 23:05:26
@author: robin huang(yuchonghuang@sina.cn)

'''
from PathUtility import IsPathExist, AllTheFilesInDir
import pandas as pd
from TradingDays import getTradingDaysWithSperate
import pandas


class ConvertToDataByDate(object):
    def __init__(self):
        self.allData = {}

    def ConverFrom(self, folder):
        if not IsPathExist(folder):
            return False

        tradingDays = getTradingDaysWithSperate()
        print tradingDays

        files = AllTheFilesInDir(folder)
        for fileName in files:
            df = pd.read_csv(fileName)
            stockID = fileName[fileName.rfind('/')+1:fileName.rfind('.')]
            for index in df.index:
                row = df.loc[index]
                s = row.drop('日期')
                s['股票代码'] = stockID
                print row.shape
                row.index[0] = u'aa'
                print row.shape
                newIndex = row.index.values[1:].insert(0, '股票代码')
                print s.reindex(newIndex)
                #print s.index




if __name__ == '__main__':
    c = ConvertToDataByDate()
    folder = u'/Volumes/Data/StockAssistant/StockData/HistoryInfo/东方财富_后复权/'
    c.ConverFrom(folder)
