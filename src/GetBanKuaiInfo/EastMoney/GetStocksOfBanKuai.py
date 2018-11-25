# coding=utf-8
'''
Created on 2018-11-21 23:15:51
@author: robin huang(yuchonghuang@sina.cn)

'''
import httplib
import json
import re
from pandas import DataFrame
import datetime


class CGetStocksOfBanKuai(object):
    def __init__(self, banKuaiId, banKuaiName):
        self._bankuaiID = banKuaiId
        self._bankuai_name = banKuaiName
        self._stockIDsOfBanKuai = None
        self._returnStartString = "varfNmaUPtx="
        self.site = 'nufm.dfcfw.com'
        self.url = "/EM_Finance2014NumericApplication/JS.aspx?type="        \
                   "CT&cmd=C.%s&sty=DCFFPBFMS&sortType=(BalFlowMain)"       \
                   "&sortRule=-1&page=1&pageSize=5000&js=varfNmaUPtx="   \
                   "{rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4"\
                   "c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.62860"\
                   "6915911589&_=1542548483587" % (banKuaiId)

    def _parseStockIDsOfBanKuai(self, data):
        if data is None:
            return False
        data = data.decode('utf_8_sig')
        size = len(self._returnStartString)
        data = data[data.find(self._returnStartString)+size:]
        data = data.replace('rank:', "\"rank\":")
        data = data.replace('pages:', "\"pages\":")
        data = data.replace('total:', "\"total\":")
        data = re.sub('\'', '\"', data)
        js = json.loads(data)
        count = js['total']
        rank = js['rank']
        allData = []
        for item in rank:
            splieted = item.split(',')
            allData.append(splieted[1:])
        day = datetime.date.today()
        zhuli = u'净流入_%04d%02d%02d' % (day.year, day.month, day.day)
        head = [u'股票代码', u'股票名称']
        head.append(zhuli)
        self._stockIDsOfBanKuai = DataFrame(allData, columns=head)
        if self._stockIDsOfBanKuai.shape[0] != count:
            print '''
            http://%s%s
            size = %d,
            count = %d,
            ''' % (self.site, self.url,
                   self._stockIDsOfBanKuai.shape[0], count)
            return False
        return True

    def GetStockIDsOfBanKuai(self):
        try:
            conn = httplib.HTTPConnection(self.site)
            conn.request("GET", self.url)
            r1 = conn.getresponse()
            if r1.status == 200 and r1.reason == 'OK':
                data = r1.read()
                if not self._parseStockIDsOfBanKuai(data):
                    print u'解析东方财富板块信息包含的证券代码信息失败!'
                    conn.close()
                    return None
                conn.close()
                return self._stockIDsOfBanKuai
            else:
                print u'获取东方财富板块信息 失败，原因:', r1.status, r1.reason
                return None
        except Exception as e:
            print e
            return None


if __name__ == '__main__':
    aa = CGetStocksOfBanKuai(u'BK04731', u'券商信托')
    print aa.GetStockIDsOfBanKuai()
