# coding=utf-8
'''
Created on 2018年11月21日

@author: robin huang(yuchonghuang@sina.cn)
'''
import httplib
import json
from pandas import DataFrame


class CGetBanKuaiInfoSummary(object):
    def __init__(self):
        # 'http://quote.eastmoney.com/centerv2/Content/Static/SidebarConfig.json'
        self.site = 'quote.eastmoney.com'
        self.url = '/centerv2/Content/Static/SidebarConfig.json'
        self._banKuaiInfo = None

    def _parseBanKuaiInfo(self, data):
        if data is None:
            return None
        self._banKuaiInfo = None
        data = data.decode('utf_8_sig')
        js = json.loads(data)
        nextNav = js['nextNav']
        res = []
        for Nav in nextNav:
            if Nav['name'] == u'沪深板块':
                for group in Nav['nextNav']:
                    groupName = group['name']
                    for y in group['gbIns']:
                        item = {}
                        item[u'板块代码'] = y['code']
                        item[u'板块名称'] = y['name']
                        item[u'所属板块'] = groupName
                        res.append(item)
        df = DataFrame(res, columns=[u'板块代码', u'板块名称', u'所属板块'])
        self._banKuaiInfo = df
        return self._banKuaiInfo

    def getMapOfBanKuai(self):
        try:
            conn = httplib.HTTPConnection(self.site)
            conn.request("GET", self.url)
            r1 = conn.getresponse()
            if r1.status == 200 and r1.reason == 'OK':
                data = r1.read()
                if self._parseBanKuaiInfo(data) is None:
                    print u'解析东方财富板块信息失败!'
                    conn.close()
                    return None
                conn.close()
                return self._banKuaiInfo
            else:
                print u'获取东方财富板块信息 失败，原因:', r1.status, r1.reason
                return None
        except Exception as e:
            print e
            return None


if __name__ == '__main__':
    bankuai = CGetBanKuaiInfoSummary()
    res = bankuai.getMapOfBanKuai()
    print res