# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import string
import os
import gettext

import __builtin__
__builtin__._ = gettext.gettext

from GeSpeakClass import GeSpeak

__author__="GeSpeak Team"

class GeSpeakWindow():
    __doc__ = """
        This class is the one that build the GTK interface for GeSpeak
    """

    def __init__(self):
        """
            All the work is made here, in the constructor
        """
        # Creating GeSpeak's object
        self.gespeak = GeSpeak()
        # Creating window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_vbox = gtk.VBox() # The main vertical box.
        # Creating menu and options
        self.menubar = self.create_menu()
        # Creating window's elements
        self.optbar1 = gtk.HBox() # The box that contais pitch, speed and language
        # Starting items of optbar1
        # Pitch in optbar1
        self.lbl_pitch = gtk.Label(_("Pitch"))
        self.optbar1.pack_start(self.lbl_pitch, expand=True, fill=True)
        self.adj_pitch = gtk.Adjustment(self.gespeak.get_pitch(), 1.0, 99.0, 1.0, 5.0, 0.0)
        self.spin_pitch = gtk.SpinButton(adjustment=self.adj_pitch, climb_rate=0.0, digits=0)
        self.spin_pitch.set_range(1, 99)
        self.optbar1.pack_start(self.spin_pitch, expand=True, fill=True)
        # Speed in optbar1
        self.lbl_speed = gtk.Label(_("Speed"))
        self.optbar1.pack_start(self.lbl_speed, expand=True, fill=True)
        self.adj_speed = gtk.Adjustment(self.gespeak.get_speed(), 30.0, 200.0, 1.0, 5.0, 0.0)
        self.spin_speed = gtk.SpinButton(adjustment=self.adj_speed, climb_rate=0.0, digits=0)
        self.spin_speed.set_range(30, 200)
        self.optbar1.pack_start(self.spin_speed, expand=True, fill=True)
        # Language in optbar1
        self.lbl_language = gtk.Label(_("Language"))
        self.optbar1.pack_start(self.lbl_language, expand=True, fill=True)
        self.cbox_language = gtk.combo_box_new_text()
        for language in self.gespeak.get_languages_list():
            self.cbox_language.append_text(language)
        self.cbox_language.set_active(0)
        self.optbar1.pack_start(self.cbox_language, expand=True, fill=True)
        # Ending optbar1
        # Startin optbar2 
        self.optbar2 = gtk.HBox() # This box contains only the voice (male or female)
        # Voices
        self.lbl_voice = gtk.Label(_("Voice") + ": ")
        self.optbar2.pack_start(self.lbl_voice, expand=False, fill=False)
        self.voice_male = gtk.RadioButton(group=None, label=_("Male"))
        self.optbar2.pack_start(self.voice_male, expand=False, fill=True)
        self.voice_female = gtk.RadioButton(group=self.voice_male, label=_("Female"))
        self.optbar2.pack_start(self.voice_female, expand=False, fill=True)
        # Ending optbar2
        # Starting the TextView area
        self.text_area = gtk.HBox()
        self.text_buffer = gtk.TextBuffer()
        self.text = gtk.TextView(buffer=self.text_buffer)
        self.text_area.pack_start(self.text, expand=True, fill=True)
        # Ending the TextView area
        #Starting the buttons bar
        self.button_bar = gtk.HBox()
        self.btn_stop = gtk.Button(_("Stop"))
        self.button_bar.pack_start(self.btn_stop, expand=True, fill=True)
      
        self.btn_talk = gtk.Button(_("Talk"))
        self.button_bar.pack_start(self.btn_talk, expand=True, fill=True)

        # Adding elements to window
        self.window.add(self.main_vbox)
        self.main_vbox.pack_start(self.menubar, expand=False, fill=True)
        self.main_vbox.pack_start(self.optbar1, expand=False, fill=True)
        self.main_vbox.pack_start(self.optbar2, expand=False, fill=True)
        self.main_vbox.pack_start(self.text_area, expand=True, fill=True)
        self.main_vbox.pack_start(self.button_bar, expand=False, fill=False)

        # Connecting signals
        self.window.connect("destroy", self.close)
        self.btn_talk.connect("clicked", self.talk)
        self.btn_stop.connect("clicked", self.stop)

        # Setting window properties
        self.window.set_title("GeSpeak " + self.gespeak.version)
        self.window.set_border_width(4)
        self.window.set_size_request(500,300)
        self.window.set_position(gtk.WIN_POS_CENTER)

        # Showing everything
        self.window.show_all()

    def main(self):
        """
            gtk.main()... this is the loop that waits for events
        """
        gtk.main()

    def create_menu(self):
        """
            This function creates the menubar of GeSpeak.
        """
        menubar_entries = (
            ( "FileMenu", None, _("File")),
            ( "Help", None, _("About")),
            ( "Open", gtk.STOCK_OPEN,
                _("Open"), "<control>o",
                _("Open a text file"),
                self.open_file),
            ( "Quit", gtk.STOCK_QUIT,
                _("Quit"), "<control>q",
                _("Quit GeSpeak"),
                self.close),
            ( "About", None,
                _("About"), "<control>a",
                _("About"),
                self.show_about),
        )
        menubar_xml = """<ui>
            <menubar name='MenuBar'>
                <menu action='FileMenu'>
                    <menuitem action='Open'/>
                    <separator/>
                    <menuitem action='Quit'/>
                </menu>
                <menu action='Help'>
                    <menuitem action='About'/>
                </menu>
            </menubar>
        </ui>"""
        actions = gtk.ActionGroup("Actions")
        actions.add_actions(menubar_entries)
        ui = gtk.UIManager()
        ui.insert_action_group(actions, 0)
        self.window.add_accel_group(ui.get_accel_group())
        try:
            mergeid = ui.add_ui_from_string(menubar_xml)
        except gobject.GError, msg:
            print("building menus failed: %s" % msg)
        return ui.get_widget("/MenuBar")

    def talk(self, widget):
        """
            This function calls GeSpeak.talk()
        """
        # Setting parameters
        self.gespeak.set_pitch(pitch=self.spin_pitch.get_value())
        self.gespeak.set_speed(speed=self.spin_speed.get_value())
        self.gespeak.set_language(language=self.cbox_language.get_active_text())
        if self.voice_male.get_active() == True :
            self.gespeak.set_voice(voice="")
        else:
            self.gespeak.set_voice(voice="+12")
        # Checking if there are selected text
        selection = self.text_buffer.get_selection_bounds()
        if selection.__len__() > 0 :
            text=self.text_buffer.get_text(selection[0],selection[1])
        else :
            text=self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter())
        self.gespeak.talk(text=text)

    def stop(self, widget):
        """
            This function calls GeSpeak.stop()
        """
        self.gespeak.stop()
    
    def open_file(self, widget):
        """
            this function opens a text file
        """
        open_file = gtk.FileChooserDialog(title=_("Select a text file to open"),
            parent=self.window, action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK),
            backend=None)
        filter = gtk.FileFilter()
        filter.set_name(_("Text files"))
        filter.add_pattern("*.txt")
        open_file.add_filter(filter)
        response = open_file.run()
        if response == gtk.RESPONSE_OK:
            text = ""
            txt_file = open(open_file.get_filename(), 'r')
            for line in txt_file:
                text += line
            self.text_buffer.set_text(text)
        open_file.destroy()

    def show_about(self, widget):
        """
            This function shows an about window
        """
        about = gtk.AboutDialog()
        about.set_name("GeSpeak")
        about.set_program_name("GeSpeak")
        about.set_version(self.gespeak.version)
        about.set_copyright("Copyright 2009 - GeSpeak Team")
        about.set_license("GPL v3 http://www.gnu.org/licenses/gpl-3.0.txt")
        about.set_website("http://gespeak.googlecode.com")
        about.set_website_label("http://gespeak.googlecode.com")
        about.set_authors(['Evaldo Junior (InFog)',"Walter Cruz"])
        about.connect("response", lambda d, r: d.destroy())
        about.show_all()

    def close(self, widget):
        """
           This function is called to close GeSpeak 
        """
        self.gespeak.exit()
        gtk.main_quit()
