# coding=utf-8
'''
Created on 2018-11-25 22:56:35
@author: robin huang(yuchonghuang@sina.cn)

'''
from StrategyTest.StrategyTestBase import CStrategyTestBase
from Strategy.BetaFilter import CBataFilter


class CBetaFilterTest(CStrategyTestBase):
    def __init__(self):
        pass

    def Test(self, param1=None, param2=None, param3=None, param4=None):
        beta = CBataFilter()
        df1 = self._readStockHistoryInfoByID(param1)
        df2 = self._readIndexHitoryInfoByID(param2)
        ret = beta.doFilterEveryDay(df1, df2, (1, 3, 13, 15, 9))
        ret[1].to_csv(u'../../../88.csv', encoding='utf_8_sig', index=False, header=True)

if __name__ == '__main__':
    test = CBetaFilterTest()
    test.Test('000001', 'BK04751')