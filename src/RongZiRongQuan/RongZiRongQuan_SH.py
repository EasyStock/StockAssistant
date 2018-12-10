# coding=utf-8
'''
Created on 2018-12-02 21:49:50
@author: robin huang(yuchonghuang@sina.cn)

'''
import httplib
import pandas as pd
import os
from PathUtility import MakeDirIfNotExist, IsFileExist


class CRongZiRongQuan_SH(object):
    def __init__(self):
        self._summary = None
        self._detail = None

    def _requestFromSSE(self, date):
        '''
        * 本栏目数据根据券商申报的数据汇总，由券商保证数据的真实、完整、准确。
        * 本日融资融券余额＝本日融资余额＋本日融券余量金额
        * 本日融资余额＝前日融资余额＋本日融资买入额－本日融资偿还额；
        * 本日融资偿还额＝本日直接还款额＋本日卖券还款额＋本日融资强制平仓额＋本日融资正权益调整－本日融资负权益调整；
        * 本日融券余量=前日融券余量+本日融券卖出数量-本日融券偿还量；
        * 本日融券偿还量＝本日买券还券量＋本日直接还券量＋本日融券强制平仓量＋本日融券正权益调整－本日融券负权益调整－本日余券应划转量；
        * 融券单位：股（标的证券为股票）/份（标的证券为基金）/手（标的证券为债券）。
        *明细信息中仅包含当前融资融券标的证券的相关数据，汇总信息中包含被调出标的证券范围的证券的余额余量相关数据。
        '''
        tmpFile = u'/tmp/tmp_%s.xls' % (date)
        site = 'www.sse.com.cn'
        url = '/market/dealingdata/overview/margin/a/rzrqjygk%s.xls' % (date)
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
            self._detail = pd.read_excel(tmpFile, 1)
            conn.close()
            os.remove(tmpFile)
        else:
            print 'getRongZiRongQuan_SH failed', r1.status, r1.reason, site+url
            conn.close()

    def getRongZiRongQuan(self, date, folder):
        if date is None or folder is None:
            return False

        summaryFolder = '%s/Summary/' % (folder)
        detailFolder = '%s/Detail/' % (folder)
        MakeDirIfNotExist(summaryFolder)
        MakeDirIfNotExist(detailFolder)
        summayFile = '%s/summary_SH_%s.csv' % (summaryFolder, date)
        detalFileName = '%s/detail_SH_%s.csv' % (detailFolder, date)

        if IsFileExist(summayFile) and IsFileExist(detalFileName):
            return True

        self._requestFromSSE(date)
        if self._summary is None or self._detail is None:
            return False

        self._summary.to_csv(summayFile, encoding='utf_8_sig', index=False)
        self._detail.to_csv(detalFileName, encoding='utf_8_sig', index=False)
        return True

    def getRongZiRongQuanByDates(self, dates, folder):
        for date in dates:
            if not self.getRongZiRongQuan(date, folder):
                print 'get %s RongZiRongQuan_SH failed!' % (date)
            else:
                print 'get %s RongZiRongQuan_SH done!' % (date)


if __name__ == '__main__':
    r = CRongZiRongQuan_SH()
    folder = '/Volumes/Data/StockAssistant/StockData/RongZiRongQuan/'
    print r.getRongZiRongQuan('20181130', folder)
