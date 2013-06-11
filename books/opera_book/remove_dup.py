#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sqlite3

def remove_dup(book):
    conn = sqlite3.connect(book)
    cursor = conn.cursor()

    cursor.execute(
        """
        delete from wordjoy where id not in
         (select id from wordjoy group by name)
        """)
    # 提交修改
    conn.commit()

    return True

if __name__ == '__main__':
    remove_dup('../wordjoy.book')
