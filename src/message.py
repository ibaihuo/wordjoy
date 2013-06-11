#!/usr/bin/env python
# coding: utf-8

import gtk
import os

def show_info(message, title = "提示", buttons = gtk.BUTTONS_OK, parent = None):
    dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, buttons)
    dialog.set_icon_from_file("../glade/wordjoy.png")
    dialog.set_title(title)
    dialog.set_markup(message)
    dialog.run()
    dialog.destroy()

    
class MessageDialog(gtk.MessageDialog):
    def __init__(self, 
            message,
            title = "提示",
            parent = None, 
            flags = 0, 
            type = gtk.MESSAGE_INFO,
            buttons = gtk.BUTTONS_YES_NO):
        gtk.MessageDialog.__init__(self, parent, flags, type, buttons)
        self.set_markup(message)
        self.set_title(title)
        self.set_icon_from_file("../glade/wordjoy.png")
