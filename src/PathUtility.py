# coding=utf-8
'''
Created on 2018年10月20日

@author: robin huang(yuchonghuang@sina.cn)
'''
import os
import shutil


def IsPathExist(path):
    if path is None:
        return False

    if os.path.exists(path) and os.path.isdir(path) is True:
        return True
    return False


def MakeDirIfNotExist(path):
    if path is None:
        return False

    if IsPathExist(path):
        return True

    os.makedirs(path)
    return True


def IsFileExist(fileName):
    if fileName is None:
        return False

    if os.path.exists(fileName) and os.path.isfile(fileName) is True:
        return True

    return False


def CopyFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!" % (srcfile)
        return False
    else:
        fpath, _ = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile, dstfile)
        return True


if __name__ == '__main__':
    pass