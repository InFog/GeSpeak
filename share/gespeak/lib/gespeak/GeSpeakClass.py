#       GeSpeakClass.py
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
import sys
import os
import commands
import string
import ConfigParser

__doc__ = """
    This is the main module of GeSpeak
    In this file is the GeSpeak class which is the one that calls eSpeak
    with the arguments from the GTK interface
"""

__author__="GeSpeak Team"

class GeSpeak:
    __doc__ = """
        This is the GeSpeak class
        it's mainly function is to call eSpeak
        with the arguments from the GTK interface

        But it also controls the preferences file which contains
        some options about de user interface
    """

    def __init__(self):
        """
            This is the constructor of the GeSpeak class
        """
        self.version = "0.4"
        self.espeak = "" # variable containing eSpeak's bin
        if self.pre_setup() == 0:
            self.load_prefs()
            self.load_langs()
        else:
            return 1

    def exit(self):
        """
            This function saves the preferences file and terminates GeSpeak
        """
        conf_file = open(self.__gespeak_conf_file, 'w')
        conf_text = []
        conf_text.append("[gespeak]\n")
        conf_text.append("amplitude = %i\n" % self.__amplitude)
        conf_text.append("pitch = %i\n" % self.__pitch)
        conf_text.append("speed = %i\n" % self.__speed)
        conf_text.append("language = %s\n" % self.__language)
        conf_file.writelines(conf_text)
        conf_file.close()

    def pre_setup(self):
        """
            This function searches for the eSpeak binary and
            the conf dir of GeSpeak (~/.gespeak)

            If the eSpeak binary isn't istalled then the value 1 is
            returned.

            If the conf dir isn't created then it will be created.

            If everything is okay then it returns 0
        """
        self.espeak = commands.getoutput("which espeak")
        self.espeak = str(self.espeak)
        if (self.espeak != ""):
            return 0
        else:
            print("eSpeak not found!")
            return 1

    def load_prefs(self):
        """
            This function reads the preferences from the prefs file
            ~/.gespeak/gespeak.xml

            If the preferences file don't exists it will be created
        """
        self.__amplitude = 10
        self.__pitch = 30
        self.__speed = 70
        self.__language = "en-us"
        self.__voice = "Male"
        self.__wavfile = ""
        gespeak_dir = os.environ["HOME"] + "/.gespeak"
        if (os.path.exists(gespeak_dir) == False) :
            os.mkdir(gespeak_dir)
        self.__gespeak_conf_file = gespeak_dir + "/gespeak.conf"
        if (os.path.exists(self.__gespeak_conf_file) == False) :
            conf_file = open(self.__gespeak_conf_file, 'w')
            conf_text = []
            conf_text.append("[gespeak]\n")
            conf_text.append("amplitude = 10\n")
            conf_text.append("pitch = 30\n")
            conf_text.append("speed = 70\n")
            conf_text.append("language = en-us\n")
            conf_file.writelines(conf_text)
            conf_file.close()
        else:
            conf_file = ConfigParser.ConfigParser()
            conf_file.read(self.__gespeak_conf_file)
            self.__amplitude = int(conf_file.get("gespeak", "amplitude"))
            self.__pitch = int(conf_file.get("gespeak", "pitch"))
            self.__speed = int(conf_file.get("gespeak", "speed"))
            self.__language = conf_file.get("gespeak", "language")

    def load_langs(self):
        """
            This function gets the languages that espeak supports
            by reading files and directories under /usr/share/espeak-data/voices
        """
        self.__languages_names = []
        languages_files_or_dirs = os.listdir('/usr/share/espeak-data/voices')
        for file_or_dir in languages_files_or_dirs :
            if file_or_dir != '!v' and file_or_dir != 'mb' :
                if os.path.isfile('/usr/share/espeak-data/voices/%s' % file_or_dir) :
                    self.load_language_from_file(lang_file='/usr/share/espeak-data/voices/%s' % file_or_dir)
                else :
                    languages_sub_files_or_dirs = os.listdir('/usr/share/espeak-data/voices/%s' % file_or_dir)
                    for sub_file_or_dir in languages_sub_files_or_dirs :
                        if os.path.isfile('/usr/share/espeak-data/voices/%s/%s' % (file_or_dir,sub_file_or_dir)) :
                            self.load_language_from_file(lang_file='/usr/share/espeak-data/voices/%s/%s' % (file_or_dir,sub_file_or_dir))

    def load_language_from_file(self, lang_file):
        lfile = open(lang_file, 'r')
        name_ok = False
        for line in lfile:
            if name_ok == False:
                if line.find('name ') != -1 :
                    name_ok = True
                    self.__languages_names.append(line.split(' ')[1].split('\n')[0])
        lfile.close()

    def get_languages_names(self):
        """
            This functios return a list of languages names supported by espeak
        """
        return self.__languages_names

    def set_amplitude(self, amplitude):
        """
            This function sets the amplitude

            Params
                Amplitude must be an integer betwwn 1 and 20
        """
        if amplitude > 0 and amplitude <= 20 :
            self.__amplitude = amplitude

    def get_amplitude(self):
        """
            This function just returns the amplitude
            an integer number
        """
        return self.__amplitude

    def set_pitch(self, pitch):
        """
           this function sets the pitch

           Params
               Pitch must be an integer between 1 and 99
        """
        if pitch > 0 and pitch < 100 :
            self.__pitch = pitch

    def get_pitch(self):
        """
            This function just returns the pitch
            an integer number
        """
        return self.__pitch

    def set_speed(self, speed):
        """
            this function sets the speed

            Params
                Speed must be an integer between 30 and 200
        """
        if speed >= 30 and speed <= 200 :
            self.__speed = speed

    def get_speed(self):
        """
            This function gets the speed
            an integer number
        """
        return self.__speed

    def set_language(self, language):
        """
            This functions sets the language
            Language must be a string in a format supported by espeak

            Examples:
            en  English
            pt  Portuguese

            For more information see espeak's manual
        """
        self.__language = language

    def get_language(self):
        """
            this function gets the language
        """
        return self.__language

    def set_voice(self, voice):
        """
            This function sets the voice

            Params
                An empty string for male

                "+12" for female

            Only some languages supports female voice
        """
        self.__voice = voice

    def get_voice(self):
        """
            this function gets the voice
        """
        return self.__voice

    def set_wav_file(self, wav_file):
        """
            This function sets the wav file to write output rather than speaking it directly
        """
        self.__wavfile = wav_file

    def write_wav_file(self, text):
        """
            This function calls to the talk function with the option to write a wav file
        """
        self.talk(text=text, wav=1)

    def talk(self, text, wav=0):
        """
            This function is called to run espeak with the parameters from UI

            Params
                text = The text you want espeak to "talk"

            Usage:
                talk("Text to talk")

            Make sure you have set up all parameters before calling this
            function
        """
        # A little easter egg
        if text == '==tell me a story==' :
            text = self.tell_a_story()
        speak_this = open("/tmp/speak_this", "w")
        text = str(text)
        speak_this.write(text)
        speak_this.close()
        espeak_command = self.espeak
        if (wav == 1):
            espeak_command += " -w " + self.__wavfile
        espeak_command += " -a " + str(self.__amplitude)
        espeak_command += " -v " + self.__language + self.__voice
        espeak_command += " -s " + str(self.__speed)
        espeak_command += " -p " + str(self.__pitch)
        espeak_command += " -f /tmp/speak_this > /dev/null &"
        os.system(espeak_command)

    def stop(self):
        """
            This function stops espeak from talking
        """
        os.system("killall espeak > /dev/null &")

    def tell_a_story(self):
        story = """
            Once time ago, in a seaside city,
            lived a little girl who loved to play with her parrot.
            And what a nice parrot it was.
            She used to sing to the parrot, and he, to yell,
            so happy was the parrot, because other people
            didn't like him, but she liked.
            The parrot really enjoyed the time with the girl.
            And then the girl grew up and got a boyfriend.
            The parrot became a little jealous,
            but the girl always had time to play and sing with him.
            Some years later the girl got married and left home.
            The parrot was alone, the girl didn't take the parrot
            to her new home.
            The parrot was alone, he didn't sing anymore, he didn't yell anymore...
        """
        return story
