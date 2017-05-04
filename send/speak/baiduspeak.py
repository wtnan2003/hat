# -*- coding: utf-8 -*-
'''''
Author         :   Peizhong Ju
Latest Update  :   2016/4/21
Function       :   Use Baidu Voice API to speak
'''
import ConfigParser
import json
import subprocess
import urllib
import urllib2
from wayspeak import word_st




config = ConfigParser.ConfigParser()
config.readfp(open('./config.ini'))
TOKEN = config.get('Baidu', 'token')
local = config.get('Dir', 'mp3')
global words


def GetVoice(word):
    words=word
    text = urllib.quote(words)
    url = 'http://tsn.baidu.com/text2audio?tex=' + text + '&cuid=b888e32e868c&lan=zh&ctp=1&tok=' + TOKEN
    rep = urllib.urlretrieve(url, local)
    CheckError()


def GetAccessToken():
    client_id = config.get('Baidu', 'client_id')
    client_secret = config.get('Baidu', 'client_secret')
    rep = urllib2.urlopen(
        'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret)
    hjson = json.loads(rep.read())
    return hjson['access_token']


def CheckError():
    global TOKEN
    file_object = open(local)
    try:
        all_the_text = file_object.read()
        if (all_the_text[0] == '{'):
            hjson = json.loads(all_the_text)
            # print hjson['err_no']
            if (hjson['err_no'] == 502):
                print 'Getting new access token...'
                TOKEN = GetAccessToken()
                config.set('Baidu', 'token', TOKEN)
                config.write(open('config.ini', "r+"))
                GetVoice()
            else:
                print all_the_text
        else:
            print '[success] ' #+ words
    finally:
        file_object.close()

#a=word_st.waytospeak('person',25,position=0)
#try:
#    words = a.encode('utf8')
#    GetVoice()
#    subprocess.call(["mplayer", "hello.mp3"],
#                    shell=False,
#                    stdout=subprocess.PIPE,
#                    stderr=subprocess.PIPE)

    # use other software to play it
#except Exception as e:
#   print "ERROR!"
#    print e