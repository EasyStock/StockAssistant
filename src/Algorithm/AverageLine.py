# coding=utf-8
'''
Created on 2018-12-02 14:45:58
@author: robin huang(yuchonghuang@sina.cn)

'''
from Algorithm.AlgorithmBase import CAlgorithmBase
import pandas as pd
import talib._ta_lib as ta
import pandas

import matplotlib.pyplot as plt

class CAverageLine(CAlgorithmBase):
    def __init__(self):
        pass

    def checkParameter(self, param1=None, param2=None, param3=None):
        if param1 is None or param2 is None:
            return False

        if not isinstance(param1, (list, tuple, pd.DataFrame)):
            return False

        return True

    def calcLastDay(self, param1=None, param2=None, param3=None):
        if not self.checkParameter(param1, param2, param3):
            return None

        raise Exception('calcLastDay not implemented')

    def calcEveryDay(self, param1=None, param2=None, param3=None):
        if not self.checkParameter(param1, param2, param3):
            return None

        if param3 is None:
            param3 = '收盘价'

        df = param1
        if isinstance(param2, (int, float)):
            key = '%s_MA%d' % (param3, param2)
            df[key] = ta.MA(df[param3].values, param2)
            return df

        if isinstance(param2, (list, tuple)):
            for day in param2:
                key = '%s_MA%d' % (param3, day)
                values = df[param3].astype(float).values
                df[key] = ta.MA(values, day)
            return df
        return None

    def MA(self, index, df, n):
        df = df.join(pd.Series(pd.rolling_mean(df[index], n),
                               name='MA' + str(n)))
        return df


if __name__ == '__main__':
    fileName = u'/Volumes/Data/StockAssistant/StockData/HistoryInfo/东方财富_后复权/001811.csv'
    outileName = u'/Volumes/Data/StockAssistant/StockData/HistoryInfo/000001_.csv'
    df = pandas.read_csv(fileName)
    line = CAverageLine()
    res = line.calcEveryDay(df, (5, 10, 20, 60))
    res = res[-200:]
    res = res.set_index('日期')
    res.plot(y=['收盘价', '收盘价_MA5','收盘价_MA10','收盘价_MA20','收盘价_MA60'],figsize=(16,9),title='20140101-20160717 MA')
    res.to_csv(outileName, encoding='utf_8_sig', index=False)
    # res.plot(y=['收盘价_MA5','收盘价_MA10','收盘价_MA20','收盘价_MA60'],figsize=(16,9),title='20140101-20160717 MA')
    plt.show()
