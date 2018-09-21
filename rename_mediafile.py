import os
import sys
import exifread
import fnmatch
import time

#用于标识已经处理过的文件，可随意修改
salt='xxxxxx'



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
        cc = 'none'

    
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
    newname = basename  + "_" + salt + "_" + mm+cc+extname
    print(filename ," to ", newname)
    os.rename(filename, newname)

def rename_video_file(filename):
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
                if fnmatch.fnmatch(filename.lower(), '*.mov') or fnmatch.fnmatch(filename.lower(), '*.mp4') :
                    #print( filename+" is a video file")
                    rename_video_file(filename)

if __name__ == '__main__':
    main()
