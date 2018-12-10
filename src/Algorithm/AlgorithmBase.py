# coding=utf-8
'''
Created on 2018-12-02 14:33:31
@author: robin huang(yuchonghuang@sina.cn)

'''


class CAlgorithmBase(object):
    def __init__(self):
        pass

    def checkParameter(self, param1=None, param2=None, param3=None):
        raise Exception('checkParameter not implemented')

    def calcLastDay(self, param1=None, param2=None, param3=None):
        raise Exception('calcLastDay not implemented')

    def calcEveryDay(self, param1=None, param2=None, param3=None):
        raise Exception('calcLastDay not implemented')

if __name__ == '__main__':
    pass
