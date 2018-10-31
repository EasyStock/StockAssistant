# coding=utf-8
'''
Created on 2018-10-31 13:39:58
@author: robin huang(yuchonghuang@sina.cn)

'''

from Strategy.FilterBase import CFilterBase
import pandas as pd

class CAlphaFilter(CFilterBase):
    def __init__(self):
        self._filterName = 'Alpha 指标'
        
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