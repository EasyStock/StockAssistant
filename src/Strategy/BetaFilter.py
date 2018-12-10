# coding=utf-8
'''
Created on 2018-10-21 22:35:02
@author: robin huang(yuchonghuang@sina.cn)

'''
from Strategy.FilterBase import CFilterBase
import pandas as pd


class CBataFilter(CFilterBase):
    def __init__(self):
        '''
        主要用途: 贝塔指标过滤器
        '''
        self._filterName = '贝塔指标过滤器'

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
        # result.index = result['日期']
        result['收盘价_涨幅'] = result['收盘价'].pct_change()
        result['收盘价_指数_涨幅'] = result['收盘价_指数'].pct_change()
        result = result.dropna()
        return result

    def _calcCorrAndBeta(self, data):
        if data.shape[0] == 1:
            return (None, 1.0*data['收盘价_涨幅'].values[-1]/data['收盘价_指数_涨幅'].values[-1])

        corr = data['收盘价_涨幅'].corr(data['收盘价_指数_涨幅'])  # 相关系数
        stda = data['收盘价_涨幅'].std()  # 标准差
        stdb = data['收盘价_指数_涨幅'].std()  # 标准差
        return (corr, corr*stda / stdb)

    def _calcOneDay(self, mergedData, rParam):
        '''
        根据 rParam 计算一天的Beta 指标
        其中 rParam 为一个列表
        '''
        corrs = []
        betas = []
        index = []
        size = len(mergedData)
        for day in rParam:
            temp = mergedData
            if size > day:
                temp = temp[-day:]
            else:
                continue
            (corr, beta) = self._calcCorrAndBeta(temp)

            corrs.append(corr)
            betas.append(beta)
            index.append(day)
        ret = pd.DataFrame()
        ret['相关系数'] = corrs
        ret['Beta值'] = betas
        ret['日期'] = index
        return ret

    def doFilterLastDay(self, data=None, lParam=None, rParam=None):
        if self._checkParameter(data, lParam, rParam) is False:
            return (False,)

        result = self._prepareData(data, lParam, rParam)
        size = len(result)
        if size <= 1:
            return (False,)
        res = self._calcOneDay(result, rParam)

        if res is None:
            return (False,)
        return (True, res)

    def doFilterEveryDay(self, data=None, lParam=None, rParam=None):
        if self._checkParameter(data, lParam, rParam) is False:
            return (False,)
        result = self._prepareData(data, lParam, rParam)
        size = len(result)
        if size <= 1:
            return (False,)

        ret = {}
        for day in rParam:
            key1 = '%03d日_相关系数' % (day)
            key2 = '%03d日_Beta值' % (day)
            dict_corr = {}
            dict_beta = {}
            for i in range(0, size-1):
                if i+day > size:
                    break
                if i == 0:
                    temp = result[-day:]
                else:
                    temp = result[-day-i: -i]
                subKey = temp['日期'].values[-1]
                # fileName = '../../../aa/%d日_%d_%s.csv' % (day, i,subKey)
                # temp.to_csv(fileName, encoding='utf_8_sig',
                #            index=False, header=True)
                (corr, beta) = self._calcCorrAndBeta(temp)
                dict_corr[subKey] = corr
                dict_beta[subKey] = beta
                #print day, subKey, corr, beta
            ret[key1] = dict_corr
            ret[key2] = dict_beta
        res = pd.DataFrame(ret, columns=sorted(ret.keys()))
        columns = ['日期']
        columns.extend(res.columns.values)
        res = res.reset_index()
        res.rename(columns={'index': '日期'}, inplace=True)
        result = pd.merge(res, result, how='left', on=['日期'])
        return (True, res)


if __name__ == '__main__':
    file1 = u'/Volumes/Data/StockAssistant/StockData/HistoryInfo/东方财富_后复权/000002.csv'
    file2 = u'/Volumes/Data/StockAssistant/StockData/HistoryInfo/东方财富_指数/上证指数.csv'

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    beta = CBataFilter()
    ret = beta.doFilterEveryDay(df1, df2, (1,3, 13, 15, 9))
    ret[1].to_csv('./88.csv', encoding='utf_8_sig', index=True, header=True)
