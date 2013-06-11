#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sqlite3

class Export():
    """导出所有单词列表
    """
    def __init__(self, database):
        """
        """
        self.__database = database
        self.__connect()

    def __connect(self):
        """
        """
        self.conn = sqlite3.connect(self.__database)
        self.cursor = self.conn.cursor()

    def get_words(self):
        """
        """
        all_list = open('all_words.list', 'w')

        self.cursor.execute(
            """
            SELECT name from wordjoy group by name""")

        words = self.cursor.fetchall()
        #print words
        for word in words:
            #print word[0]
            all_list.write(word[0] + '\n')
        all_list.close()

if __name__ == '__main__':
    e = Export('../wordjoy.book')
    e.get_words()
