# coding=utf-8
'''
Created on 2018年12月2日

@author: robin huang(yuchonghuang@sina.cn)
'''
import httplib
import pandas as pd
import os
from PathUtility import MakeDirIfNotExist, IsFileExist


class CRongZiRongQuan_SZ(object):
    def __init__(self):
        self._summary = None
        self._detail = None

    def _requestFromSZSE_Summary(self, date):
        '''
        说明：1. 本报表基于证券公司报送的融资融券余额数据汇总生成，其中：
        本日融资余额(元)=前日融资余额＋本日融资买入-本日融资偿还额
        本日融券余量(股)=前日融券余量＋本日融券卖出量-本日融券买入量-本日现券偿还量
        本日融券余额(元)=本日融券余量×本日收盘价
        本日融资融券余额(元)=本日融资余额＋本日融券余额；
        2. 2014年9月22日起，“融资融券交易总量”数据包含调出标的证券名单的证券的融资融券余额。
        '''
        tmpFile = u'/tmp/SZ_Summary_tmp_%s.xls' % (date)
        site = 'www.szse.cn'
        url = '/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1837_xxpl&txtDate=%s&tab2PAGENO=1&random=0.6403259429591708&TABKEY=tab1'%(date)
        conn = httplib.HTTPConnection(site)
        conn.request("GET", url)
        r1 = conn.getresponse()
        if r1.status == 200 and r1.reason == 'OK':
            Rawdata = r1.read()
            with open(tmpFile, 'w') as f:
                f.write(Rawdata)
                f.close()
            df0 = pd.read_excel(tmpFile, 0)
            self._summary = df0[:1]
            conn.close()
            os.remove(tmpFile)
        else:
            print 'getRongZiRongQuan_SZ failed', r1.status, r1.reason, site+url
            conn.close()

    def _requestFromSZSE_Detail(self, date):
        '''
        说明：1. 本报表基于证券公司报送的融资融券余额数据汇总生成，其中：
        本日融资余额(元)=前日融资余额＋本日融资买入-本日融资偿还额
        本日融券余量(股)=前日融券余量＋本日融券卖出量-本日融券买入量-本日现券偿还量
        本日融券余额(元)=本日融券余量×本日收盘价
        本日融资融券余额(元)=本日融资余额＋本日融券余额；
        2. 2014年9月22日起，“融资融券交易总量”数据包含调出标的证券名单的证券的融资融券余额。
        '''
        tmpFile = u'/tmp/SZ_Detail_tmp_%s.xls' % (date)
        site = 'www.szse.cn'
        url = '/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1837_xxpl&txtDate=%s&tab2PAGENO=1&random=0.8500878261472522&TABKEY=tab2'%(date)
        conn = httplib.HTTPConnection(site)
        conn.request("GET", url)
        r1 = conn.getresponse()
        if r1.status == 200 and r1.reason == 'OK':
            Rawdata = r1.read()
            with open(tmpFile, 'w') as f:
                f.write(Rawdata)
                f.close()
            self._detail = pd.read_excel(tmpFile, 0)
            conn.close()
            os.remove(tmpFile)
        else:
            print 'getRongZiRongQuan_SZ failed', r1.status, r1.reason, site+url
            conn.close()

    def getRongZiRongQuan(self, date, folder):
        if date is None or folder is None:
            return False

        summaryFolder = '%s/Summary/' % (folder)
        detailFolder = '%s/Detail/' % (folder)
        MakeDirIfNotExist(summaryFolder)
        MakeDirIfNotExist(detailFolder)
        summayFile = '%s/summary_SZ_%s.csv' % (summaryFolder, date)
        detalFileName = '%s/detail_SZ_%s.csv' % (detailFolder, date)

        if IsFileExist(summayFile) and IsFileExist(detalFileName):
            return True

        self._requestFromSZSE_Summary(date)
        self._requestFromSZSE_Detail(date)

        if self._summary is None or self._detail is None:
            return False

        self._summary.to_csv(summayFile, encoding='utf_8_sig', index=False)
        self._detail.to_csv(detalFileName, encoding='utf_8_sig', index=False)
        return True

    def getRongZiRongQuanByDates(self, dates, folder):
        for date in dates:
            if not self.getRongZiRongQuan(date, folder):
                print 'get %s RongZiRongQuan_SZ failed!' % (date)
            else:
                print 'get %s RongZiRongQuan_SZ done!' % (date)


if __name__ == '__main__':
    sz = CRongZiRongQuan_SZ()
    sz._requestFromSZSE_Summary('2018-12-07')
    print sz._summary
    sz._requestFromSZSE_Detail('2018-12-07')
    print sz._detail