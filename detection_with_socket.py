# !/usr/bin/env python
# -*- coding=utf-8 -*-
import keras
import pickle
import cv
import socket
import sys

from sklearn import preprocessing
from sklearn.externals import joblib

from regression_for_distance import reg_distance
sys.path.append("..")
from videotest import VideoTest
from ssd import SSD300 as SSD
import os
import struct
import threading
import numpy as np

input_shape = (300, 300, 3)
# global class_names_2send  # ---------define the class to speaker
# class_names_2send = ''  # ---------send the class to speaker
# Change this if you run with other classes than VOC
class_names = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
               "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
               "tvmonitor"];
NUM_CLASSES = len(class_names)

model = SSD(input_shape, num_classes=NUM_CLASSES)

# Change this path if you want to use your own trained weights
model.load_weights('/home/wxf/weights_SSD300.hdf5')
print 'load comlete'

"""
file: recv.py
socket service
"""
vid_test = VideoTest(class_names, model, input_shape)


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET ipv4
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('192.168.0.105', 6666))
        s.listen(10)
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Waiting connection...'

    while 1:
        conn, addr = s.accept()
        deal_data(conn, addr)


def deal_data(conn, addr):
    print 'Accept new connection from {0}'.format(addr)
    # conn.settimeout(500)
    conn.send('Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        print fileinfo_size
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('<128sl0l', buf)
            fn = filename.strip('\00')
            new_filename = os.path.join('./', 'new_' + fn)
            print 'file new name is {0}, filesize if {1}'.format(new_filename, filesize)
            new_filename = os.path.abspath(new_filename)
            print new_filename
            try:
                recvd_size = 0  # 定义已接收文件的大小
                fp = open(new_filename, 'wb')
                print 'start receiving...'

                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = conn.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = conn.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
                print 'end receive...'
                print 'strat detection'
                class_names, area = vid_test.run(new_filename)
                print 'area is : %s'%area
                #area=preprocessing.scale(area)
                #area = np.array([area])
                distance = 11980 * pow(area,-0.5371)+0.3389
                #charmProjects/untitled2/ssd_keras/svr_rbf2.pkl')
                #predict_distance=svr_rbf2.predict(area)
                #print predict_distance
                #distance=(predict_distance)[0]
                print class_names
                print "distnace is %s "%distance
                conn.sendall(class_names)
                conn.recv(1024)
                conn.sendall(str(distance))
                conn.recv(1024)
            except Exception as e:
                conn.close()
                print "ERROR!"
                print e

        conn.close()

        break


socket_service()
