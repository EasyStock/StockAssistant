# coding=utf-8
'''
Created on 2018年10月18日

@author: robin huang(yuchonghuang@sina.cn)
'''
from GetStockBasicInfo import GetStockBasicInfo_FromSZ
from GetStockBasicInfo import GetStockBasicInfo_FromSH
import Configuration
import time
import PathUtility
import pandas as pd


def GetBasicInfo(folder=Configuration.BasicInfo_DefaultFolder):
    PathUtility.MakeDirIfNotExist(folder)
    res_SH = False
    res_SZ = False
    hisotryPath = u'%s/History/' % (Configuration.BasicInfo_DefaultFolder)
    t = time.localtime()

    src_fileName_SH = '%s/%s.csv' % (
                Configuration.BasicInfo_DefaultFolder,
                Configuration.BasicInfo_Name_SH)
    dest_fileName_SH = '%s/%s_%4d_%02d_%02d.csv' % (
                                    hisotryPath,
                                    Configuration.BasicInfo_Name_SH,
                                    t.tm_year,
                                    t.tm_mon,
                                    t.tm_mday)

    src_fileName_SZ = '%s/%s.csv' % (
        Configuration.BasicInfo_DefaultFolder,
        Configuration.BasicInfo_Name_SZ)

    dest_fileName_SZ = '%s/%s_%4d_%02d_%02d.csv' % (
                                    hisotryPath,
                                    Configuration.BasicInfo_Name_SZ,
                                    t.tm_year,
                                    t.tm_mon,
                                    t.tm_mday)

    for _ in range(5):
        res_SH = GetStockBasicInfo_FromSH.GetAllStockInfoOfShangHai(folder)
        res_SZ = GetStockBasicInfo_FromSZ.GetAllStockInfoFromShenZhen(folder)
        if res_SH and res_SZ:
            PathUtility.CopyFile(src_fileName_SH, dest_fileName_SH)
            PathUtility.CopyFile(src_fileName_SZ, dest_fileName_SZ)
            break


def ReadBasicInfoFromFile():
    src_fileName_SH = '%s/%s.csv' % (
                Configuration.BasicInfo_DefaultFolder,
                Configuration.BasicInfo_Name_SH)

    src_fileName_SZ = '%s/%s.csv' % (
        Configuration.BasicInfo_DefaultFolder,
        Configuration.BasicInfo_Name_SZ)

    df_sh = pd.read_csv(src_fileName_SH)
    df_sz = pd.read_csv(src_fileName_SZ)
    result = df_sh.append(df_sz)

    return result


if __name__ == '__main__':
    df = ReadBasicInfoFromFile()
    df.to_csv('/Volumes/Data/StockData/aa/aa.csv', encoding='utf_8_sig', index=False, header=True)
