# coding=utf-8
'''
Created on 2018年11月24日

@author: robin huang(yuchonghuang@sina.cn)
'''
from GetBanKuaiInfoSummary import CGetBanKuaiInfoSummary
from GetStocksOfBanKuai import CGetStocksOfBanKuai
from Configuration import HistoryInfo_DefaultFolder
from PathUtility import MakeDirIfNotExist


def GetBanKuaiSummary(folder=None, saveToFile=False):
    bankuai = CGetBanKuaiInfoSummary()
    res = bankuai.getMapOfBanKuai()
    if res is None:
        print 'GetBanKuaiSummary Failed!'
    if saveToFile:
        if folder is None:
            folder = u'../../%s/板块/' % (HistoryInfo_DefaultFolder)
        fileName = u'%s/板块分类.csv' % (folder)
        res.to_csv(fileName, encoding='utf_8_sig', index=False, header=True)
    return res


def GetStockIDsOfOneBanKuai(banKaiID, banKuaiName):
    bankuai = CGetStocksOfBanKuai(banKaiID, banKuaiName)
    res = bankuai.GetStockIDsOfBanKuai()
    return res


def GetAllBanKuaiInfos(folder):
    if folder is None:
        folder = u'../../%s/板块/' % (HistoryInfo_DefaultFolder)

    MakeDirIfNotExist(folder)
    bankuai = CGetBanKuaiInfoSummary()
    banKuaiInfos = bankuai.getMapOfBanKuai()
    if banKuaiInfos is None:
        print 'GetBanKuaiInfoSummary Failed'
        return False
    fileName = u'%s/板块分类.csv' % (folder)
    banKuaiInfos.to_csv(fileName, encoding='utf_8_sig', index=False)

    for row in banKuaiInfos.itertuples():
        banKaiID = row[1]
        banKuaiName = row[2]
        groupName = row[3]
        destFolder = u'%s/%s' % (folder, groupName)
        MakeDirIfNotExist(destFolder)
        info = CGetStocksOfBanKuai(banKaiID, banKuaiName)
        stockIDs = info.GetStockIDsOfBanKuai()
        fileName = u'%s/%s_%s.csv' % (destFolder, banKuaiName, banKaiID)
        stockIDs.to_csv(fileName, encoding='utf_8_sig', index=False)

    print 'done'
    return True


if __name__ == '__main__':
    #GetBanKuaiSummary()
    #print GetStockIDsOfOneBanKuai(u'BK04731', u'券商信托')
    GetAllBanKuaiInfos(None)