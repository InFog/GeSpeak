#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       gespeak.py
#
#       This file is part of the GeSpeak project
#       http://gespeak.googlecode.com
#
#       Copyright 2009 Evaldo Junior (InFog) <junior@casoft.info>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

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
