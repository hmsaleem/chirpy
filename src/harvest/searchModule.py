#!/usr/bin/python


import os, sys, shutil, codecs
if sys.stdout.encoding == None:
    os.putenv("PYTHONIOENCODING",'UTF-8')
    os.execv(sys.executable,['python']+sys.argv)

#-------------------------------------------------------------------------------------------------------------

import profileModule
import helpModule
import datetime
from urllib import quote_plus
from urllib import unquote
import json, time, errno
import twitter

def searching(configs, query, output_file, output_dir, num):
	print 'Getting Configurations' 
	time.sleep(0.5)
	ppath = configs['ppath']
	lpath = configs['lpath']
	root = configs['dpath']
	if root == 'False':
        	root = './'
	
	helpModule.make_outdir(root+output_dir)
	
	print 'Configuring Files'
	time.sleep(0.5)
	outfile = root + output_dir + '/' + output_file

	fo = open(outfile, 'w')
	fo.close()

	print 'Encoding Query'
	time.sleep(0.5)
	enc_query = quote_plus(query.encode('UTF-8'), safe=':/')

        pid = str(os.getpid())
        logfile = lpath+pid+'.searchlog'
	
	print 'Retrieving Twitter Profile' 
        time.sleep(0.5)
	profile = profileModule.get_profile(ppath, lpath)
        profilepath = ppath+profile+'.profile'
        deets = profileModule.get_deets(profilepath)

	print 'Authorizing Twitter Profile'
	time.sleep(0.5)
	auth = twitter.oauth.OAuth(deets["access_token"], deets["access_token_secret"], deets["consumer_key"], deets["consumer_secret"])
	twitter_api = twitter.Twitter(auth=auth)

	count = 100

	print 'Starting Search'
	time.sleep(0.5)
	search_results = twitter_api.search.tweets(q=enc_query, count=count)

	with open(logfile, 'a') as fo:
		fo.write(profile+'\n')
		fo.write(query+'\n')

	statuses = search_results['statuses']
	counter = 0
	tweets = 0

	while True:
		counter+=len(statuses)
		print "Tweets Collected: ", counter
 
		if int(num)!= 0 and counter >= int(num):
			print 'Deadline Reached \nExiting'
			break		

		helpModule.write_to_file(statuses, outfile)
		statuses = []

		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e:
			break

		kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])

		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']

		with open(logfile, 'a') as fo:
			fo.write(str(tweets)+'\n')

		time.sleep(6)

	print 'Writing To File'
	helpModule.write_to_file(statuses, outfile)

	os.remove(logfile)
	
	return

