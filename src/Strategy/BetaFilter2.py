# coding=utf-8
'''
Created on 2018-10-31 13:39:58
@author: robin huang(yuchonghuang@sina.cn)

'''

from Strategy.FilterBase import CFilterBase
import pandas as pd


class CBetaFilter2(CFilterBase):
    def __init__(self):
        self._filterName = 'Beta 指标2'

    def _checkParameter(self, data=None, lParam=None, rParam=None):
        '''
        检查参数:
        data 必须是一个DataFrame
        lParam 必须是一个DataFrame
        rParam 必须是一个列表
        '''
        if data is None or lParam is None or rParam is None:
            return False

        if isinstance(data, pd.DataFrame) is False:
            return False

        if isinstance(lParam, pd.DataFrame) is False:
            return False

        if isinstance(rParam, (list, tuple)) is False:
            return False

        return True

    def _prepareData(self, data=None, lParam=None, rParam=None):
        '''
        准备数据:
        合并个股与大盘的数据，计算涨幅
        '''
        sub1 = pd.DataFrame()
        sub1['日期'] = data['日期']
        sub1['收盘价'] = data['收盘价']
        sub1.index = sub1['日期']

        sub2 = pd.DataFrame()
        sub2['日期'] = lParam['日期']
        sub2['收盘价_指数'] = lParam['收盘价']
        sub2.index = sub2['日期']

        result = pd.merge(sub1, sub2, how='left', on=['日期'])
        result.index = result['日期']
        result = result.dropna()
        return result

    def doFilterLastDay(self, data=None, lParam=None, rParam=None):
        '''
        算法思路: 与指数相比，得出与指数相比的强弱值
        data: 股票数据
        lParam: 指数数据
        rParam: 参数N， 要获取N 的贝塔系数
        收盘价/N日前的收盘价/(大盘的收盘价/N日前的大盘的收盘价) >1
        表示：
        1. 如果大盘跌， 我比大盘跌的更少，例如 0.95/0.92
        2. 如果大盘涨， 我比大盘涨的更多， 例如 1.08/1.06
        符号判断法则:
        '''
        pass

    def doFilterEveryDay(self, data=None, lParam=None, rParam=None):
        pass


if __name__ == '__main__':
    pass