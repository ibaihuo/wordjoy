#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import gtk

from db import ConnectDB
from StringIO import StringIO
import urllib2
from xml.etree.ElementTree import ElementTree, Element, tostring

class CreateBook():
    """创建新书类
    """
    def __init__(self, database, table):

        db = ConnectDB(database)
#        db.create_new_table(table)

        missing = open("missing", "a+")
        
        for word in open('words.list'):
            word = word.rstrip()
            print '正在添加单词……  ' , word
            word_xml = GetWord()
            word_dic = word_xml.get_word_xml(word)
            if word_dic == None:
                print '%s Not Found' % word
                missing.write(word + '\n')
                continue
            else:
                #print word_dic
                db.insert_a_dict(word_dic)

class GetWord():
    def __init__(self):
        pass
#        self.get_word_xml("greyhound")

    def __xml_parse(self, word):
        """解析测试
        """
        word_dic = {}

        word_dic['name'] = word[0].getchildren()[0].text

        if word[0].find('pron') is not None:
            word_dic['pronounce'] = word[0].getchildren()[2].text
            word_dic['meaning'] = word[0].getchildren()[3].text
        else:
            word_dic['pronounce'] = ""
            word_dic['meaning'] = word[0].getchildren()[2].text

        word_dic['sentence'] = []
        sen_all = word[0].findall("sent")
        if sen_all is not None:
            for sen_all_child in sen_all:
                en = sen_all_child.getchildren()[0].text
                zh = sen_all_child.getchildren()[1].text
                word_dic['sentence'].append((en, zh))

        # print word_dic
        return word_dic
    def get_word_xml(self, word):
        # mini版本
        # word_page = "http://dict.cn/mini.php?q=" + word
        # xml版本
        word_page = "http://dict.cn/ws.php?q=" + word
        content = urllib2.urlopen(word_page).read()
        # print content
        try:
            content = unicode(content, 'gbk').encode("utf8")
        except UnicodeDecodeError:
            return None
        # print content

        # 删除掉原来文件中编码指示，否则会出错
        # content = content.replace(' encoding="GBK" ', '')
        # 直接去掉文件头声明
        content = content.replace('<?xml version="1.0" encoding="GBK" ?>', '')

        tree = ElementTree()
        tree.parse(StringIO(content))

        word = tree.getiterator("dict")

        if word[0].getchildren()[0].text != "Not Found":

            audio = word[0].find("audio")
            if audio is not None:
                word[0].remove(audio)
                
            # print tostring(word[0], 'utf8')
            return self.__xml_parse(word)

            # 按字符串打印
            # return tree
        else:
            return None

if __name__ == '__main__':
#    GetWord()
    database = "../wordjoy.book"
    table = "wordjoy"
    CreateBook(database, table)
