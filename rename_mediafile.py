#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import exifread
import fnmatch
import time
import ffmpeg
import logging

#用于标识已经处理过的文件，可随意修改
salt='xxxxxx'
logfilename='rename'+time.strftime('%Y%m%d%H%M%S')+'.log'
logging.basicConfig(filename = logfilename, level = logging.INFO, format = '%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger()



def renname_jpg_file(filename):
    f = open(filename, 'rb')
    tags = exifread.process_file(f)
    #ext name
    extname = os.path.splitext(filename)[1]

    #base name
    basename = os.path.splitext(filename)[0]
    #create time
    try:

        ctime = tags['EXIF DateTimeOriginal']
        cc = str(ctime)
        cc = cc.replace(' ', '_')
        cc = cc.replace(':', '_')
    except:
        try:
            ctime = tags['Image DateTime']
            cc = str(ctime)
            cc = cc.replace(' ', '_')
            cc = cc.replace(':', '_')
        except:
            cc = 'none'
    #image make
    try:
        cmake = tags['Image Make']
        cm = str(cmake)
        cm = cm.replace(' ', '_')
        cm = cm.replace(':', '_')
        cm = cm.replace('/', '_')
    except:
        cm = None
    
    #model name
    try:
        cmodel = tags['Image Model']
        mm = str(cmodel)
        mm = mm.replace(' ', '_')
        mm = mm.replace(':', '_')
        mm = mm.replace('/', '_')
        
    except:
        mm = 'none'

    #filename=org+salt+mm+cc.jpg
    newname = basename  + "_" + salt + "_" + cm + "_" + mm + "_" + cc + extname
    print(filename ," to ", newname)
    logger.info("from "+filename+" to "+newname)
    f.close()
    os.rename(filename, newname)

def rename_video_file(filename):
    # tags = ffmpeg.probe(filename)["streams"]
    # ctime = tags[0]['tags']['creation_time']
    ctime = time.localtime(os.path.getmtime(filename))
    createtime = str(ctime.tm_year)+"_"+str(ctime.tm_mon)+"_"+str(ctime.tm_mday)+"_"+str(ctime.tm_hour)+"_"+str(ctime.tm_min)
    #ext name
    extname = os.path.splitext(filename)[1]

    #base name
    basename = os.path.splitext(filename)[0]
    #create time
    #filename=org+salt+mm+cc.jpg

    newname= basename + "_" + salt + "_" + createtime + extname
    print(filename +" to "+ newname)
    logger.info("from "+filename+" to "+newname)

    os.rename(filename, newname)


#def get_model_from_jpg(filename):


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
            if 'jpg' in filename.lower():
                if salt in filename:
                    print(filename+'以经变更过名称')
                else:
                    renname_jpg_file(filename)

                #print( filename+" is a jpg file.")
            else:
                if fnmatch.fnmatch(filename.lower(), '*.mov') or fnmatch.fnmatch(filename.lower(), '*.mp4')  or fnmatch.fnmatch(filename.lower(), '*.m4v'):
                    #print( filename+" is a video file")
                    rename_video_file(filename)

if __name__ == '__main__':
    main()
