#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pickle
import sqlite
import wordpath

class Record():
    """用户当前记录的单词组
    """
    interval_day = (0, 1, 1, 2, 4, 7, 14)
    def __init__(self):
        """
        """
        self.record_file = open(wordpath.RECORD, 'rb')

    def set_next_day(self, times, first = None):
        """根据interval时间间隔列表和当前的次数(time)，自动设置下
        次复习时间。first参数只用于第一次产生复习时间"""
        today = datetime.date.today()

        if first:
            next_day = today + datetime.timedelta(1)
        else:   
            next_day = today + datetime.timedelta(self.interval_day[times + 1])

        return next_day
        

    def save_current_record(self, words_list, select_word_list):
        """保存用户当前的记录
        """
        # current_record = StringIO.StringIO()
        record_file = open(wordpath.RECORD, 'w')
        
        for word_name in select_word_list:
            for word_complete in words_list:
                if word_name == word_complete['name']:
                    pickle.dump(word_complete, record_file)

        record_file.close()

    def save_reciting_record(self):
        """将用户当前正在背诵的单词保存到数据库
        """
        words_list = self.get_current_record()
        print words_list

        db = sqlite.ConnectDB(wordpath.BOOK_PATH + 'reciting.book')
        # db.create_new_table('reciting')
        db.insert_data('reciting', words_list)
        
    def get_current_record(self):
        """获取当前用户的记录文件
        """
        self.words_list = []

        Loading = True
        while Loading:
            try:
                word = pickle.load(self.record_file)
                # print record_dic
            except pickle.UnpicklingError:
                print "UnpicklingError"
                pass
            except EOFError:
                Loading = False
                print "End of file"
            else:
                self.words_list.append(word)

        return self.words_list

if __name__ == '__main__':
    re = Record()
#    print re.get_current_record()
    print re.save_reciting_record()
