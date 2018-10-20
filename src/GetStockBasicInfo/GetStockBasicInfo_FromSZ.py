# coding=utf-8
'''
Created on 2018年10月17日

@author: robin huang(yuchonghuang@sina.cn)
'''
import httplib
import pandas as pd


def StringToInt(value):
    return int(value.replace(',', ''))


def GetAllStockInfoFromShenZhen(folder):
    '''
    从深交所网站上获取所有在深交所上市股票信息，包括：
    '股票代码'，'股票名称','总股本(股)'，'流通股本(股)','上市日期'
    '''
    if folder is None:
        return False

    site = 'www.szse.cn'
    url = '/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID='\
          '1110&tab2PAGENUM=1&ENCODE=1&TABKEY=tab2'
    try:
        conn = httplib.HTTPConnection(site)
        conn.request("GET", url)
        r1 = conn.getresponse()
        if r1.status == 200 and r1.reason == 'OK':
            Rawdata = r1.read()
            tmpFileName = u'/tmp/tmp.csv'
            f = open(tmpFileName, 'w+')
            f.write(Rawdata)
            f.close()
            df = pd.read_excel(tmpFileName)
            sub = df.iloc[:, [5, 6, 8, 9, 7]].copy()
            head = [u'股票代码', u'股票名称', u'总股本(股)', u'流通股本(股)', u'上市日期']
            sub.iloc[:, 0] = sub.iloc[:, 0].map(lambda x: '%06d' % (int(x)))
            sub.iloc[:, 2] = map(StringToInt, sub.iloc[:, 2])
            sub.iloc[:, 3] = map(StringToInt, sub.iloc[:, 3])
            sub.columns = head
            tmpName = u'深圳交易所所有股票列表.csv'
            path = u'%s/%s' % (folder, tmpName)
            sub.to_csv(path, encoding='utf_8_sig', index=False, header=True)
            conn.close()
            print u'获取深圳交易所所有股票成功！总共:%d' % (sub.shape[0])
            return True
        else:
            print u'获取深圳交易所所有股票 失败,原因', r1.status, r1.reason
            return False

    except Exception as e:
        print e
        return False


if __name__ == '__main__':
    GetAllStockInfoFromShenZhen(u'/Volumes/Data/StockData/aa/')
