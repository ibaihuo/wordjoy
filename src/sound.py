#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import sys
import subprocess
from wordpath import *

def read(word):
    word = word.lower()                 # 如单词：English,在语音库中只存为：e/english.wav
    try:
        subprocess.Popen(["aplay","/usr/share/WyabdcRealPeopleTTS/%s/%s.wav" % (word[0], word)])
    except OSError:
        print '你的系统没有安装alsa工具，不能发音。'

def play(type):
    try:
        subprocess.Popen(["aplay", SOUND_PATH + "%s.wav" % type])
    except OSError:
        print '你的系统没有安装alsa工具，不能发音。'

if __name__ == "__main__":
    read('love')
    play("menushow")
