# coding=utf-8
'''
Created on 2018-10-21 10:58:20
@author: robin huang(yuchonghuang@sina.cn)

'''
import re
import httplib
import json
import pandas as pd
import Configuration
import datetime
from Configuration import HistoryInfo_DefaultFolder
import PathUtility
import pandas


class CGetHistoryDataFrom_EastMoney(object):
    def __init__(self):
        '''
        cycle = 'k' 日K线
        cycle = 'wk' 周K线
        cycle = 'mk' 月K线
        cycle = 'm5k' 5分钟K线
        cycle = 'm15k' 15分钟K线
        cycle = 'm30k' 30分钟K线
        cycle = 'm60k' 60分钟K线
        '''
        self.site = 'pdfm.eastmoney.com'
        self.jsonHead = 'jsonp1539703490452'
        self.connection = None
        self.cycle = 'k'  # 需要的是日K线

    def FormatStockID(self, stockID):
        stockID = '%06d' % (int(stockID))
        if re.findall("^60\d", str(stockID)):
            return '%06d1' % (int(stockID))
        elif re.findall("^00\d", str(stockID)):
            return '%06d2' % (int(stockID))
        elif re.findall("^30\d", str(stockID)):
            return '%06d2' % (int(stockID))
        else:
            return None

    def FormatStockType(self, stockTpye):
        if stockTpye == 'hfq':
            return 'ba'
        elif stockTpye == 'qfq':
            return 'fa'
        elif stockTpye == 'bfq':
            return ''
        else:
            return 'ba'

    def FormatURL(self, stockID, dType):
        stockID = self.FormatStockID(stockID)
        if stockID is None:
            return None
        # 默认为后复权
        t = self.FormatStockType(dType)
        url = '/EM_UBG_PDTI_Fast/api/js?'\
            'token=4f1862fc3b5e77c150a2b985b12db0fd&'\
            'rtntype=6&' \
            'id=%s&'\
            'type=%s&'\
            'authorityType=%s'\
            '&cb=%s' % (
                stockID,
                self.cycle,
                t,
                self.jsonHead
            )
        return url

    def ConnectToEastSite(self):
        if self.connection is None:
            self.connection = httplib.HTTPConnection(self.site)
        return self.connection

    def GetDataFromSite(self, url):
            self.connection.request("GET", url)
            r1 = self.connection.getresponse()
            if r1.status == 200 and r1.reason == 'OK':
                rawData = r1.read()
                if rawData.find('{stats:false}') != -1:
                    return None
                return rawData
            return None

    def ParseJosonData(self, data):
        js = json.loads(data)
        allHistory = js['data']
        allData = []
        for x in allHistory:
            data = x.split(',')
            allData.append(data)
        df = pd.DataFrame(allData)
        columns = ['日期', '开盘价', '收盘价', '最高价',
                   '最低价', '成交量', '成交额', '振幅', '换手率(%)']
        df.columns = columns[:df.shape[1]]
        return df

    def GetHistoryDataWithStockID(self, stockID, dType=None, folder=None):
        '''
        从东方财富网获取股票ID为stockID 的历史信息
        http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?token=4f1862fc3b5e77c150a2b985b12db0fd&rtntype=6&id=0007032&type=k&authorityType=ba&cb=jsonp1540037821141
        dType = 'hfq' 为后复权
        dType = 'qfq' 为前复权
        dType = 'bfq' 为不复权
        '''
        if dType is None:
            dType = 'hfq'

        if folder is None:
            folder = Configuration.HistoryInfo_DefaultFolder

        try:
            self.ConnectToEastSite()
            url = self.FormatURL(stockID, dType)
            rawData = self.GetDataFromSite(url)
            if rawData is None:
                print 'get from http://%s%s error' % (self.site, url)
                return False
            df = self.ParseJosonData(rawData[len(self.jsonHead)+1:-1])
            fileName = '%s/%06d.csv' % (folder, int(stockID))
            df.to_csv(fileName, encoding='utf_8_sig', index=False, header=True)
            return True
        except Exception as e:
            print '%s, http://%s%s' % (e, self.site, url)
            return False

    def GetHistoryDataWithStockIDs(self, allStocks, dType=None, folder=None):
        if folder is None:
            folder = HistoryInfo_DefaultFolder

        if dType == 'hfq':
            folder = u'%s/东方财富_后复权' % (folder)
        elif dType == 'qfq':
            folder = u'%s/东方财富_前复权' % (folder)
        elif dType == 'bfq':
            folder = u'%s/东方财富_不复权' % (folder)

        PathUtility.MakeDirIfNotExist(folder)
        if isinstance(allStocks, pandas.DataFrame):
            stockIDs = allStocks.iloc[:, 0].values  # 第0列是股票代码
        elif isinstance(allStocks, (list, tuple)):
            stockIDs = allStocks

        size = len(stockIDs)
        index = 0
        start = datetime.datetime.now()
        for stockID in stockIDs:
            t = datetime.datetime.now()
            res = self.GetHistoryDataWithStockID(stockID, dType, folder)
            index = index + 1
            end = datetime.datetime.now()
            current = (end-t).total_seconds()
            allTime = (end-start).total_seconds()
            print '准备获取代码为: %06d 的历史信息,结果:%s,' \
                  '当前第%d, 总共:%d, 当前用时:%f 秒, 总共用时:%f 秒' % (
                   int(stockID), res, index, size, current, allTime)

        print '完成!'


if __name__ == '__main__':
    stockIDs = ['601818', '300033', 590, 2062]
    eastMoney = CGetHistoryDataFrom_EastMoney()
    eastMoney.GetHistoryDataWithStockIDs(stockIDs, 'bfq')
