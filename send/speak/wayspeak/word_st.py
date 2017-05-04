#!/usr/bin/env python
# -*- coding: utf-8 -*-

def waytospeak(class_names, distance,classnum=1,  position=0, *args, **kwargs):
    word_class_names = {'cat': '猫', 'car': '车', 'person': '人', 'motobike': '摩托车', 'bike': "自信车"}
    class_names = word_class_names[class_names]
    if classnum >= 3:
        classnum = 3
    word_classnum = {1: '一个', 2: '两个', 3: '许多'}
    classnum = word_classnum[classnum]
    if position >= 3:
        position = 3

    position_classnum = {0: "前方", -1: "左前方", 1: "右前方"}
    position = position_classnum[position]

    word_templete = position + str(distance) + '米' + '有' + classnum + class_names
    return word_templete.decode('utf-8')
