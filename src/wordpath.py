#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

GLADE_PATH = "../glade/"
BOOK_PATH = "../books/joy_books/"

SOUND_PATH = "../sound/"

JOY_PATH = os.path.join(os.path.expanduser("~"), ".wordjoy") # .wordjoy目录
USER_BOOK_PATH = os.path.join(JOY_PATH, "books")

RECORD = os.path.join(JOY_PATH, "record")
FINISHED = os.path.join(JOY_PATH, "finished")
