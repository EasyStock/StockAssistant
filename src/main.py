# coding=utf-8
'''
Created on 2018年10月20日

@author: robin huang(yuchonghuang@sina.cn)
'''
from GetStockBasicInfo import GetStockBasicInfoMgr
from GetStockHistoryData.DailyK.EastMoney import CGetHistoryDataFrom_EastMoney,\
    CGetHistoryDataOfIndexFrom_EastMoney
from GetBanKuaiInfo.EastMoney.BanKuaiInfosMgr import GetBanKuaiSummary
from pandas import DataFrame


def GetAllIndexsInfo():
    data = [
        [u'0000011', u'上证指数', u'常规指数'],
        [u'0000021', u'A股指数', u'常规指数'],
        [u'0000031', u'B股指数', u'常规指数'],
        [u'0000161', u'上证50', u'常规指数'],
        [u'0003001', u'沪深300', u'常规指数'],
        [u'3990062', u'创业板指', u'常规指数'],
        [u'3990012', u'深证成指', u'常规指数']
        ]
    banKuai = GetBanKuaiSummary()
    if banKuai is None:
        print 'GetAllIndexsInfo failed!'
    data.extend(banKuai.values.tolist())
    df = DataFrame(data, columns=[u'指数代码', u'指数名称', u'所属板块'])
    df = df.drop(u'所属板块', 1)
    return df


def GetAllHistroyData_FromEastMoney(dType):
    df = GetStockBasicInfoMgr.ReadBasicInfoFromFile()
    east = CGetHistoryDataFrom_EastMoney.CGetHistoryDataFrom_EastMoney()
    east.GetHistoryDataWithStockIDs(df, dType)


def GetAllHistoryIndexData_FromeEastMoney():
    indexInfos = GetAllIndexsInfo()
    east = CGetHistoryDataOfIndexFrom_EastMoney.CGetHistoryDataOfIndexFromEastMoney()
    east.GetHistoryDataWithIndexIDs(indexInfos)


def GetBasicInfo():
    GetStockBasicInfoMgr.GetBasicInfo()

if __name__ == '__main__':
#     GetAllIndexsInfo()
#     GetBasicInfo()
#     GetAllHistroyData_FromEastMoney('hfq')
    GetAllHistoryIndexData_FromeEastMoney()
