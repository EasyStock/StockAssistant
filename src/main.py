# coding=utf-8
'''
Created on 2018年10月20日

@author: robin huang(yuchonghuang@sina.cn)
'''
from GetStockBasicInfo import GetStockBasicInfoMgr
from GetStockHistoryData.DailyK.EastMoney import CGetHistroryDataFrom_EastMoney


def GetAllHistroyData(dType):
    df = GetStockBasicInfoMgr.ReadBasicInfoFromFile()
    east = CGetHistroryDataFrom_EastMoney.CGetHistoryDataFrom_EastMoney()
    east.GetHistoryDataWithStockIDs(df, dType)


if __name__ == '__main__':
    GetAllHistroyData('hfq')
