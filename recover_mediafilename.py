#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import exifread
import fnmatch
import time

#用于标识已经处理过的文件，可随意修改
salt='xxxxxx'

def recover_mediafilename(filename):
    old=filename.split('_'+salt)[0]
    extname = os.path.splitext(filename)[1]
    oldname = old+extname
    print(filename ," to ", oldname)
    os.rename(filename, oldname)


def main():
    top_dir = sys.argv[1]
    if os.path.exists(top_dir) == False:
        print("not exists")
        return
    if os.path.isdir(top_dir) == False:
        print("not a dir")
        return
    for dir_path, subpaths, files in os.walk(top_dir):
        for file in files:
            filename = os.path.join(dir_path, file)
            if salt in filename:
                #执行文件名恢复操作
                #print(filename+'以经变更过名称')
                recover_mediafilename(filename)


if __name__ == '__main__':
    main()
