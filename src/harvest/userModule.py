#!/usr/bin/python


import os, sys, shutil, codecs
if sys.stdout.encoding == None:
    os.putenv("PYTHONIOENCODING",'UTF-8')
    os.execv(sys.executable,['python']+sys.argv)

#-------------------------------------------------------------------------------------------------------------

import profileModule
import helpModule
import datetime
import json, time, errno
import tweepy

def user_history(configs, user, output_dir):
	print 'Accessing User', user
	time.sleep(0.5)
	print 'Getting Configurations' 
	time.sleep(0.5)
	ppath = configs['ppath']
	lpath = configs['lpath']
	root = configs['dpath']
	if root == 'False':
        	root = './'

	helpModule.make_outdir(root+output_dir)
	
	output_file = user+'.txt'

	print 'Configuring Files'
	time.sleep(0.5)
	outfile = root + output_dir + '/' + output_file

	fo = open(outfile, 'w')
	fo.close()

        pid = str(os.getpid())
        logfile = lpath+pid+'.userlog'
	
	print 'Retrieving Twitter Profile' 
        time.sleep(0.5)
	profile = profileModule.get_profile(ppath, lpath)
        profilepath = ppath+profile+'.profile'
        deets = profileModule.get_deets(profilepath)

	print 'Authorizing Twitter Profile'
	time.sleep(0.5)
	auth = tweepy.OAuthHandler(deets["consumer_key"], deets["consumer_secret"])
    	auth.set_access_token(deets["access_token"], deets["access_token_secret"])
    	twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
	
	count = 200
	status = []

	print 'Extracting User Tweets'
	time.sleep(0.5)
	timeline_results = twitter_api.user_timeline(screen_name = user, count=count)

	with open(logfile, 'a') as fo:
		fo.write(profile+'\n')
		fo.write(user+'\n')

   	status.extend(timeline_results)
	oldest = status[-1]['id'] - 1

	while len(timeline_results) > 0:
        	timeline_results = twitter_api.user_timeline(screen_name = user, count=count, max_id=oldest)
        	status.extend(timeline_results)
        	oldest = status[-1]['id'] - 1

        	print 'Tweets Collected: ', len(status)

		with open(logfile, 'a') as fo:
                        fo.write(str(len(status))+'\n')

		time.sleep(6)

	print 'Writing To File'
	helpModule.write_to_file(status, outfile)

	os.remove(logfile)
	
	return

