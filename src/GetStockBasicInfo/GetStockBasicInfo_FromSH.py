# coding=utf-8
'''
Created on 2018年10月17日

@author: robin huang(yuchonghuang@sina.cn)
'''
import httplib
import json
from pandas import DataFrame


def GetAllStockInfoOfShangHai(folder):
    '''
    从上交所网站上获取所有在上交所上市股票信息，包括：
    '股票代码'，'股票名称','总股本(股)'，'流通股本(股)','上市日期'
    '''

    if folder is None:
        return False

    site = 'query.sse.com.cn'
    url = '/security/stock/getStockListData2.do?&' \
          'isPagination=true&stockCode=&csrcCode=' \
          '&areaName=&stockType=1&pageHelp.cacheSize='\
          '1&pageHelp.beginPage=1&pageHelp.pageSize=3000&'\
          'pageHelp.pageNo=1&_=1481792573174'
    head = {'referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Accept-Encoding': 'gzip, deflate, sdch',
            }
    try:
        conn = httplib.HTTPConnection(site)
        conn.request("GET", url, headers=head)
        r1 = conn.getresponse()
        if r1.status == 200 and r1.reason == 'OK':
            data1 = r1.read()
            js = json.loads(data1)
            fileName = u'上海交易所所有股票列表.csv'
            allData = []
            head = [u'股票代码', u'股票名称', u'总股本(股)', u'流通股本(股)', u'上市日期']
            allData.append(head)
            results = js[u'result']
            for data in results:
                rowData = [
                    data[u'SECURITY_CODE_A'],
                    data[u'SECURITY_ABBR_A'],
                    int(float(data[u'totalShares'])*10000),
                    int(float(data[u'totalFlowShares'])*10000),
                    data[u'LISTING_DATE']
                    ]
                allData.append(rowData)
            df = DataFrame(allData)
            path = u'%s/%s' % (folder, fileName)
            df.to_csv(path, encoding='utf_8_sig', index=False, header=False)
            conn.close()
            print u'获取上海交易所所有股票成功！总共:%d' % (
                js[u'pageHelp'][u'total'])
            return True
        else:
            print u'获取上海交易所所有股票 失败，原因:', r1.status, r1.reason
            return False
    except Exception as e:
        print e
        return False


if __name__ == '__main__':
    GetAllStockInfoOfShangHai(u'/Volumes/Data/StockData/aa/')
