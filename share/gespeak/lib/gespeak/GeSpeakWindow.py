# -*- coding: utf-8 -*-
#
#       GeSpeakWindow.py
#
#       This file is part of the GeSpeak project
#       http://gespeak.googlecode.com
#
#       Copyright 2009 Evaldo Junior (InFog) <junior@casoft.info>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
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
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import string
import os
import gettext
from os.path import abspath, dirname, join, pardir, exists


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
        # The file to write eSpeak's output
        self.wav_file = ""
        # Creating window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_vbox = gtk.VBox() # The main vertical box.
        # Creating menu and options
        self.menubar = self.create_menu()
        # Creating window's elements
        self.optbar1 = gtk.HBox() # The box that contais pitch, speed and language
        # Starting items of optbar1
        # Amplitude in optbar1
        self.lbl_amplitude = gtk.Label(_("Amplitude"))
        self.optbar1.pack_start(self.lbl_amplitude, expand=True, fill=True)
        self.adj_amplitude = gtk.Adjustment(self.gespeak.get_amplitude(), 1.0, 20.0, 1.0, 2.0, 0.0)
        self.spin_amplitude = gtk.SpinButton(adjustment=self.adj_amplitude, climb_rate=0.0, digits=0)
        self.spin_amplitude.set_range(1, 20)
        self.optbar1.pack_start(self.spin_amplitude, expand=True, fill=True)
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
        active_language = 1
        i = 0
        for language in self.gespeak.get_languages_names():
            self.cbox_language.append_text(language)
            if language == self.gespeak.get_language():
                active_language = i
            i += 1
        self.cbox_language.set_active(active_language)
        self.optbar1.pack_start(self.cbox_language, expand=True, fill=True)
        # Ending optbar1
        # Starting optbar2 (Male and Female Voices)
        self.optbar2 = gtk.HBox() # This box contains only the voice (male or female)
        # Voices
        self.lbl_voice = gtk.Label(_("Voice") + ": ")
        self.optbar2.pack_start(self.lbl_voice, expand=False, fill=False)
        txt_male = _("Male")
        self.rbutton_voice_male = gtk.RadioButton(group=None, label=txt_male)
        self.optbar2.pack_start(self.rbutton_voice_male, expand=False, fill=True)
        txt_female = _("Female")
        self.rbutton_voice_female = gtk.RadioButton(group=self.rbutton_voice_male, label=txt_female)
        self.optbar2.pack_start(self.rbutton_voice_female, expand=False, fill=True)
        # Ending optbar2
        # Starting optbar3 (wav file)
        self.optbar3 = gtk.HBox()
        txt_wav_file = _("Write output to WAV file.")
        self.cbutton_wav_file = gtk.CheckButton(label=txt_wav_file)
        self.optbar3.pack_start(self.cbutton_wav_file, expand=False, fill=True)
        self.lbl_wav_filename = gtk.Label("")
        self.optbar3.pack_start(self.lbl_wav_filename, expand=False, fill=True)
        # Starting the TextView area
        self.text_area = gtk.HBox()
        self.text_buffer = gtk.TextBuffer()
        self.text = gtk.TextView(buffer=self.text_buffer)
        self.text_area.pack_start(self.text, expand=True, fill=True)
        hscroll = gtk.HScrollbar(adjustment=None)
        vscroll = gtk.VScrollbar(adjustment=None)
        self.text_area.set_scroll_adjustments(None, None)
        # Ending the TextView area
        #Starting the buttons bar
        self.button_bar = gtk.HBox()
        self.btn_stop = gtk.Button(stock=gtk.STOCK_MEDIA_STOP)
        self.button_bar.pack_start(self.btn_stop, expand=True, fill=True)

        self.btn_talk = gtk.Button(stock=gtk.STOCK_MEDIA_PLAY)
        self.button_bar.pack_start(self.btn_talk, expand=True, fill=True)

        self.btn_write = gtk.Button(stock=gtk.STOCK_MEDIA_RECORD)
        self.button_bar.pack_start(self.btn_write, expand=True, fill=True)

        # This VBox is just for visual effect
        self.body_vbox = gtk.VBox()
        self.body_vbox.set_border_width(4)

        # Adding elements to window
        self.window.add(self.main_vbox)
        self.main_vbox.pack_start(self.menubar, expand=False, fill=True)
        self.main_vbox.pack_start(self.body_vbox, expand=True, fill=True)
        self.body_vbox.pack_start(self.optbar1, expand=False, fill=True)
        self.body_vbox.pack_start(self.optbar2, expand=False, fill=True)
        self.body_vbox.pack_start(self.optbar3, expand=False, fill=True)
        self.body_vbox.pack_start(self.text_area, expand=True, fill=True)
        self.body_vbox.pack_start(self.button_bar, expand=False, fill=False)

        # Connecting signals
        self.window.connect("destroy", self.close)
        self.cbutton_wav_file.connect("clicked", self.choose_wav_file)
        self.btn_talk.connect("clicked", self.talk)
        self.btn_stop.connect("clicked", self.stop)
        self.btn_write.connect("clicked", self.write_wav)

        # Setting window properties
        self.window.set_title("GeSpeak " + self.gespeak.version)
        self.window.set_border_width(0)
        self.window.set_size_request(600,300)
        self.window.set_position(gtk.WIN_POS_CENTER)

        # Setting window's icon
        ICON_PATH = abspath(join(dirname(__file__), pardir, pardir, pardir, 'icons', 'gespeak.png'))
        icon = gtk.gdk.pixbuf_new_from_file(ICON_PATH)
        self.window.set_icon(icon)

        # Showing everything
        self.window.show_all()

        # Hiding the write button
        self.btn_write.hide()

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
            ( "Help", None, _("Help")),
            ( "Open", gtk.STOCK_OPEN,
                _("Open"), "<control>o",
                _("Open a text file"),
                self.open_file),
            ( "Quit", gtk.STOCK_QUIT,
                _("Quit"), "<control>q",
                _("Quit GeSpeak"),
                self.close),
            ( "About", gtk.STOCK_ABOUT,
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

    def change_output_mod(self, mod=0, file=''):
        """
            This function is used to change GeSpeak's output.

            Available mods are:
            0 : Normal speaking to sound device
            1 : Write output to a WAV file

            'file' must be a path to a WAV file
        """
        if mod == 0 :
            self.lbl_wav_filename.set_label("")
            self.btn_talk.show()
            self.btn_stop.show()
            self.btn_write.hide()
        else :
            self.lbl_wav_filename.set_label(self.wav_file)
            self.btn_talk.hide()
            self.btn_stop.hide()
            self.btn_write.show()


    def choose_wav_file(self, widget):
        """
            This function is called when the CheckButton "write output to wav file" is clicked.

            If this CheckButton is enabled a gtk openfile dialog is used to choose the file to write
            and the Talk and Stop buttons are hidden to show a "Write" button.
        """
        if self.cbutton_wav_file.get_active() == True :
            title_open_wav_file_dialog = _("Select a wav file to write")
            dialog_write_wav_file = gtk.FileChooserDialog(title=title_open_wav_file_dialog,
                parent=self.window, action=gtk.FILE_CHOOSER_ACTION_SAVE,
                buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK),
                backend=None)
            filter = gtk.FileFilter()
            filter.set_name(_("WAV files"))
            filter.add_pattern("*.wav")
            dialog_write_wav_file.add_filter(filter)
            response = dialog_write_wav_file.run()
            if response == gtk.RESPONSE_OK :
                self.wav_file = dialog_write_wav_file.get_filename()
                # Checking if file exists...
                if exists(self.wav_file) :
                    exists_message = gtk.Label(_("The choosen file already exists, overwrite it?"))
                    dialog_exists = gtk.Dialog(_("File overwrite"), self.window, 0,(
                        gtk.STOCK_OK, gtk.RESPONSE_OK,
                        gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
                    dialog_exists.vbox.pack_start(exists_message)
                    exists_message.show()
                    response_overwrite_file = dialog_exists.run()
                    if response_overwrite_file == gtk.RESPONSE_OK :
                        self.change_output_mod(mod=1, file=self.wav_file)
                    else :
                        self.change_output_mod(mod=0)
                        self.cbutton_wav_file.set_active(False)
                    dialog_exists.destroy()
                else :
                    self.change_output_mod(mod=1)
            else :
                self.wav_file = ""
                self.change_output_mod(mod=0)
                self.cbutton_wav_file.set_active(False)
            dialog_write_wav_file.destroy()
        else :
            self.change_output_mod(mod=0)

    def set_all_params(self):
        """
            This function set all the parameters for eSpeak from GeSpeak's interface and
            returns the text to speak.
        """
        self.gespeak.set_amplitude(amplitude=self.spin_amplitude.get_value())
        self.gespeak.set_pitch(pitch=self.spin_pitch.get_value())
        self.gespeak.set_speed(speed=self.spin_speed.get_value())
        self.gespeak.set_language(language=self.cbox_language.get_active_text())
        if self.rbutton_voice_male.get_active() == True :
            self.gespeak.set_voice(voice="")
        else:
            self.gespeak.set_voice(voice="+12")
        # Checking if there are selected text
        selection = self.text_buffer.get_selection_bounds()
        if selection.__len__() > 0 :
            text=self.text_buffer.get_text(selection[0],selection[1])
        else :
            text=self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter())
        return text

    def talk(self, widget):
        """
            This function calls GeSpeak.talk()
        """
        # Setting parameters
        text = self.set_all_params()
        self.gespeak.talk(text=text)

    def write_wav(self, widget):
        """
            This function is used to write the eSpeak's output to a wav file
        """
        text = self.set_all_params()
        if os.path.isfile(self.wav_file) :
            overwrite_dialog = gtk.Dialog(_("The file '%s' already exists\nOverwrite it?"), self, 0, (
                gtk.STOCK_OK, gtk.RESPONSE_OK,
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            )
            overwrite_dialog.run()
        self.gespeak.set_wav_file(wav_file=self.wav_file)
        self.gespeak.write_wav_file(text=text)
        done_message = _("The output was written to '%s'") % self.wav_file
        done_dialog = gtk.MessageDialog(self.window,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_OK, done_message)
        done_dialog.run()
        done_dialog.destroy()

    def stop(self, widget):
        """
            This function calls GeSpeak.stop()
        """
        self.gespeak.stop()

    def open_file(self, widget):
        """
            this function opens a text file
        """
        title_open_text_file_dialog = "Select a text file to open"
        open_file = gtk.FileChooserDialog(title=title_open_text_file_dialog,
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
        about.set_authors([ _('GeSpeak Team'), '- Evaldo Junior (InFog)'])
        ICON_PATH = abspath(join(dirname(__file__), pardir, pardir, pardir, 'icons', 'gespeak.png'))
        icon = gtk.gdk.pixbuf_new_from_file(ICON_PATH)
        about.set_icon(icon)
        about.connect("response", lambda d, r: d.destroy())
        about.show_all()

    def close(self, widget):
        """
           This function is called to close GeSpeak
        """
        self.stop(widget)
        self.gespeak.exit()
        gtk.main_quit()
