#!/usr/bin/env python
#-*- coding:utf-8 -*-

import codecs
#import wordpath
import sqlite3

class ConnectDB():
    """连接数据库
    """
    
    def __init__(self, database):
        """

        Arguments:
        - `database`:数据库相应路径
        """
        self._database = database
        self.__connect()

    def __connect(self):
        """连接数据库函数
        
        Arguments:
        - `self`:
        """
        self.conn = sqlite3.connect(self._database)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_words(self):
        """获得单词
        """
        self.cursor.execute(
            """
            SELECT * FROM  wordjoy
            """)
        #print self.cursor.fetchone()

        word_list = []

        for row in self.cursor:
            word = {}
            #print row
            word['name'] = row['name']
            word['pronounce'] = row['pronounce']
            word['meaning'] = row['meaning']
            word['sen_en_1'] = row['sen_en_1']
            word['sen_zh_1'] = row['sen_zh_1']
            word['sen_en_2'] = row['sen_en_2']
            word['sen_zh_2'] = row['sen_zh_2']
            word['sen_en_3'] = row['sen_en_3']
            word['sen_zh_3'] = row['sen_zh_3']
            word_list.append(word)

        return word_list
#             print row['sen_en_1']
#             print codecs.encode(row['meaning'], 'utf8')
        
    def insert_data(self, table, words_list):
        """
        """
        for word in words_list:
            print word
            self.cursor.execute("INSERT INTO %s values(NULL, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?)" % table,
                                (word['name'],
                                 word['pronounce'],
                                 word['meaning'],
                                 word['sen_en_1'],
                                 word['sen_zh_1'],
                                 word['sen_en_2'],
                                 word['sen_zh_2'],
                                 word['sen_en_3'],
                                 word['sen_zh_3'],
                                 ))
        self.conn.commit()

    def insert_a_dict(self, word_dic):
        """
        """
        word = word_dic
        
        while len(word['sentence']) < 3:
            word['sentence'].append(("",""))

        self.cursor.execute("INSERT INTO wordjoy values(NULL, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     (word['name'],
                                     word['pronounce'],
                                     word['meaning'],
                                     word['sentence'][0][0],
                                     word['sentence'][0][1],
                                     word['sentence'][1][0],
                                     word['sentence'][1][1],
                                     word['sentence'][2][0],
                                     word['sentence'][2][1]))

        self.conn.commit()

    def create_new_table(self, table):
        """创建新数据表
        """
        self.cursor.execute(
            """
            CREATE TABLE %s (
            id integer PRIMARY KEY,
            name varchar(20) NOT NULL,
            status integer NOT NULL, 
            pronounce varchar(20) NOT NULL, 
            meaning varchar(200), 
            sen_en_1 varchar(100),
            sen_zh_1 varchar(200), 
            sen_en_2 varchar(100), 
            sen_zh_2 varchar(200), 
            sen_en_3 varchar(100), 
            sen_zh_3 varchar(200))
            """ % table)


if __name__ == '__main__':
    db = ConnectDB(wordpath.BOOK_PATH + 'test/beginner.book')
#    db.get_words()
#    db.insert()

    print db.get_words()
