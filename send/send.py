#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""
from speak import baiduspeak
import socket
import os
import sys
import struct
from compress import com_Image
from PIL import Image
from speak import word_st
import subprocess
import ConfigParser
import json
import subprocess
import urllib
import urllib2

import brotli

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print msg
        sys.exit(1)

    a=s.recv(1024)
    print type(a)
    print a

    while 1:
        filepath = ('/home/wxf/compressfolder/dog.5.jpg')
        #filepath = ('/home/wxf/data/validation/cats/cat.1123.jpg')
        print filepath
        #sImg = Image.open(filepath)
        #w, h = sImg.size
        #dImg = sImg.resize((w / 2, h / 2), Image.ANTIALIAS)
        #dImg.save(filepath)
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath),
                                os.stat(filepath).st_size)
            s.send(fhead)
            print 'client filepath: {0}'.format(filepath)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print '{0} file send over...'.format(filepath)
                    break
                s.send(data)
        else:
            print 'file is not exist'
            s.close()
            break
        global classname
        classname=s.recv(1024)
        print 'classname is %s'%classname
        s.close()
        break


if __name__ == '__main__':
    socket_client()
    print 'outofclassname is %s'%classname
    a = word_st.waytospeak(classname, 0.5, position=-1)
    words = a.encode('utf8')
    print words
    baiduspeak.GetVoice(words)
    print words

    subprocess.call(["mplayer", "./speak/hello.mp3"],
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

        # use other software to play it
    #except Exception as e:
    #    print "ERROR!"
    #    print e
