'''
@uthor: Haji Mohammad Saleem

Initialise all the directories and 
Create and read a config file for the chirpy module.

'''

import ConfigParser
import os.path
import os
from os.path import expanduser

#-------------------------------------------------------------------------------------

def make_dir(path):
        if not os.path.exists(path):
                os.mkdir(path, 0777)
                os.chmod(path, 0777)

	return

def init_dir():
	home = expanduser("~")
	basepath = home+'/.chirpy/'
	#set paths
	path1 = basepath+'profiles'
	path2 = basepath+'logs'
	#create directories
	make_dir(basepath)
	make_dir(path1)
	make_dir(path2)

	return

def create_config():
	Config = ConfigParser.ConfigParser()
	home = expanduser("~")
	
	path1 = home+'/.chirpy/profiles/'
        path2 = home+'/.chirpy/logs/'

	cfgfilepath = home+'/.chirpy/chirpy.config'
	#create config file if not present
	cfgfile = open(cfgfilepath,'w')

	# add the settings to the structure of the file, and lets write it out...
	Config.add_section('ppath')
	Config.set('ppath','Path',path1)

	Config.add_section('lpath')
	Config.set('lpath','Path',path2)

	Config.add_section('dpath')
	Config.set('dpath','Path',False)

	Config.write(cfgfile)
	cfgfile.close()

	return

def read_config():
	Config = ConfigParser.ConfigParser()
        home = expanduser("~")

        cfgfilepath = home+'/.chirpy/chirpy.config'
	if not os.path.isfile(cfgfilepath):
		create_config()
	
	Config.read(cfgfilepath)
	
	configDict = {}

	for section in Config.sections():
        	path = Config.get(section, 'Path')
        	configDict[section] = path
	return configDict

#-------------------------------------------------------------------------------------
if __name__ == "__main__":
	init_dir()
	create_config()

