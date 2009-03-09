#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   Thanks to this guy I could internationalize GeSpeak =)
#   http://lucumr.pocoo.org/2007/6/10/internationalized-pygtk-applications2
#
def main():
    from os.path import abspath, dirname, join, pardir
    
    SHARED_FILES = abspath(join(dirname(__file__), pardir, pardir))
    LOCALE_PATH = join(SHARED_FILES, 'i18n')
    RESOURCE_PATH = join(SHARED_FILES, 'res')
    
    GETTEXT_DOMAIN = 'GeSpeak'

    # setup PyGTK by requiring GTK2
    import pygtk
    pygtk.require('2.0')

    # set up the gettext system and locales
    from gtk import glade
    import gettext
    import locale

    locale.setlocale(locale.LC_ALL, '')
    for module in glade, gettext:
        module.bindtextdomain(GETTEXT_DOMAIN, LOCALE_PATH)
        module.textdomain(GETTEXT_DOMAIN)
        
    # register the gettext function for the whole interpreter as "_"
    import __builtin__
    __builtin__._ = gettext.gettext
        
    # importing GeSpeak stuff...
    from GeSpeakClass import GeSpeak
    from GeSpeakWindow import GeSpeakWindow

    __author__="GeSpeak Team"

    __doc__ = """
        Here is called the interface and GeSpeak
    """

    window = GeSpeakWindow()
    window.main()
