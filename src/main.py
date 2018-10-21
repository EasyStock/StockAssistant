# coding=utf-8
'''
Created on 2018年10月20日

@author: robin huang(yuchonghuang@sina.cn)
'''
from GetStockBasicInfo import GetStockBasicInfoMgr
from GetStockHistoryData.DailyK.EastMoney import CGetHistoryDataFrom_EastMoney,\
    CGetHistoryDataOfIndexFrom_EastMoney


def GetAllHistroyData_FromEastMoney(dType):
    df = GetStockBasicInfoMgr.ReadBasicInfoFromFile()
    east = CGetHistoryDataFrom_EastMoney.CGetHistoryDataFrom_EastMoney()
    east.GetHistoryDataWithStockIDs(df, dType)


def GetAllHistoryIndexData_FromeEastMoney():
    east = CGetHistoryDataOfIndexFrom_EastMoney.CGetHistoryDataOfIndexFromEastMoney()
    east.GetHistoryDataWithIndexIDs()



if __name__ == '__main__':
    #GetAllHistroyData_FromEastMoney('hfq')
    GetAllHistoryIndexData_FromeEastMoney()
