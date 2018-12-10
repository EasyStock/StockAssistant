# coding=utf-8
'''
Created on 2018-10-21 13:39:13
@author: robin huang(yuchonghuang@sina.cn)

'''
import httplib
import json
import pandas as pd
import Configuration
from Configuration import HistoryInfo_DefaultFolder
import PathUtility


class CGetHistoryDataOfIndexFromEastMoney(object):
    def __init__(self):
        self.site = 'pdfm.eastmoney.com'
        self.jsonHead = 'fsData1540097283937_89020652'
        self.connection = None
        self.cycle = 'k'

    def FormatIndexURL(self, indexID):
        '''
        格式化指数的URL，指数的indexID 第7位为证券交易所，1为上交易所， 2为深交所
        '''
        if indexID is None:
            return None
        # 默认为后复权
        url = '/EM_UBG_PDTI_Fast/api/js?id=%s&'\
              'TYPE=%s&js=fsData1540097283937_89020652((x))&rtntype=5&'\
              'isCR=false&authorityType=fa&fsData1540097283937_89020652='\
              'fsData1540097283937_89020652' % (
                indexID,
                self.cycle)
        return url

    def ConnectToEastSite(self):
        if self.connection is None:
            self.connection = httplib.HTTPConnection(self.site)
        return self.connection

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

    def GetDataFromSite(self, url):
            self.connection.request("GET", url)
            r1 = self.connection.getresponse()
            if r1.status == 200 and r1.reason == 'OK':
                rawData = r1.read()
                if rawData.find('{stats:false}') != -1:
                    return None
                return rawData
            return None

    def GetHistoryDataWithIndexID(self, stockID, folder=None):
        '''
        从东方财富网获取股票ID为stockID 的历史信息
        http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000161&TYPE=wk&js=fsData1540097283937_89020652((x))&rtntype=5&isCR=false&authorityType=fa&fsData1540097283937_89020652=fsData1540097283937_89020652
        '''
        if folder is None:
            folder = Configuration.HistoryInfo_DefaultFolder

        url = self.FormatIndexURL(stockID)
        try:
            self.ConnectToEastSite()
            rawData = self.GetDataFromSite(url)
            if rawData is None:
                print 'get from http://%s%s error' % (self.site, url)
                return False
            df = self.ParseJosonData(rawData[len(self.jsonHead)+1:-1])
            fileName = u'%s/%s.csv' % (folder, stockID)
            df.to_csv(fileName, encoding='utf_8_sig', index=False, header=True)
            return True
        except Exception as e:
            print '%s, http://%s%s' % (e, self.site, url)
            return False

    def GetHistoryDataWithIndexIDs(self, indexInfos, folder=None):
        if folder is None:
            folder = u'%s/东方财富_指数' % (HistoryInfo_DefaultFolder)

        PathUtility.MakeDirIfNotExist(folder)
        for row in indexInfos.itertuples():
            indexID = row[1]
            indexName = row[2]
            print indexID, indexName
            self.GetHistoryDataWithIndexID(indexID, folder)

if __name__ == '__main__':
    index = CGetHistoryDataOfIndexFromEastMoney()
    #index.GetHistoryDataWithIndexIDs()
    print index.GetHistoryDataWithIndexID(u'BK08111', u'/Volumes/Data/StockAssistant/',u'超级品牌')