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
        self.version = "0.4b"
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
            This function gets the languages that espeak support

            It need some adjusts... A good one is to make languages names more
            human readable...
        """
        self.__languages_list = []
        commands.getoutput("espeak --voices | grep -v \"VoiceName\" | cut -f 4 -d \ > /tmp/es_voices")
        es_voices = open("/tmp/es_voices")
        for voice in es_voices:
            voice = voice.replace("\n", "") # replacing newlines...
            self.__languages_list.append(voice)
        es_voices.close()
        commands.getoutput("rm /tmp/es_voices")

    def get_languages_list(self):
        """
            This functios return a list of languages supported by espeak
        """
        return self.__languages_list

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
