#!/usr/bin/env python

__author__ = 'SaleemSaddm'

import os
import sys
import shutil
import codecs
if sys.stdout.encoding == None:
	os.putenv("PYTHONIOENCODING",'UTF-8')
	os.execv(sys.executable,['python']+sys.argv)

sys.dont_write_bytecode = True

x = os.path.dirname(os.path.realpath(__file__))

#-------------------------------------------------------------------------------------------------------------

from logModule import ref_logs
from configModule import read_config
import profileModule
from searchModule import searching
from userModule import user_history
import parseModule
import streamModule

import argparse
import signal
import subprocess
import ConfigParser
import tweepy

configs = read_config()
ref_logs(configs['lpath'])

#-------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("options", help = "Available: search, user, stream, stream_list, stream_remove, profile_add, profile_list, profile_remove, tophash, parse")
parser.add_argument("-i", "--in", help="input file", action="store", dest = 'input_file')
parser.add_argument("-f", "--fo", help="output file", action="store", dest = 'output_file')
parser.add_argument("-o", "--op", help="output dir", action="store", dest = 'output_dir')
parser.add_argument("-k", "--kw", help="keyword", action="store", dest = 'query')
parser.add_argument("-u", "--us", help="username", action="store", dest = 'user')
parser.add_argument("-n", "--nm", help="tweet limit / hashtag count", action="store", type=int, dest = 'num')
parser.add_argument("-d", "--dy", help="number of days", action="store", dest = 'days')
parser.add_argument("-p", "--pd", help="process id", action="store", dest = 'pid')
args = parser.parse_args()

#-------------------------------------------------------------------------------------------------------------


if args.options == 'search':
    	if not args.query or not args.output_dir or not args.output_file:
		print 'Missing Parameters'
		print 'Requires -k keyword, -o ouput dir, -f output file  and optional -n max number of tweets'

	else:
		output_file = args.output_file
		output_dir = args.output_dir
		query = args.query
		
		if args.num:
			num = args.num
		else:
			num = 0

		searching(configs, query, output_file, output_dir, num)	


elif args.options == 'user':
	if not args.user or not args.output_dir:
                print 'Missing Parameters'
                print 'Requires -u user, -o ouput dir'

        else:
                output_dir = args.output_dir
                user = args.user
		
		try:
                	user_history(configs, user, output_dir)
		
		except tweepy.error.TweepError as e:
                	print 'Terminating'
                	print e

elif args.options == 'parse':
        if not args.input_file:
                print 'Missing Parameters'
                print 'Requires -i input file and optional -f ouput file -u user -k keyword'

        else:
		infile = args.input_file

		if args.output_file:
			outfile = args.output_file
		else:
			outfile = infile.split('.')[0]+'_csvfile.csv'

		if args.query:
			query = args.query
		else:
			query = False

		if args.user:
			uname = args.user
		else:
			uname = False

		parseModule.create_csv(infile, outfile, query, uname)

elif args.options == 'tophash':
	if not args.input_file:
                print 'Missing Parameters'
                print 'Requires -i input file and optional -n number of hashtags'

        else:
                infile = args.input_file

                if args.num:
                        num = args.num
                else:
                        num = 100

                parseModule.hash_list(infile, num)

elif args.options == 'profile_list':
	profileModule.plist(configs['lpath'], configs['ppath'])
	
elif args.options == 'profile_add':
        profileModule.padd(configs['ppath'])

elif args.options == 'profile_remove':
        profileModule.pdel(configs['ppath'])

elif args.options == 'stream':
        if not args.days or not args.query or not args.output_dir or not args.output_file:
                print 'Missing Parameters'
                print 'Requires -k keyword, -o ouputdir, -d number of days, -f output file '
        else:
                print 'Stream Started'
		subprocess.Popen(['python', x+'/streamer.py', '-d', args.days, '-o', args.output_dir, '-f', args.output_file, '-k', args.query])

elif args.options == 'stream_list':
        streamModule.list_runs(configs['lpath'])

elif args.options == 'stream_remove':
        if not args.pid:
                print 'Missing Parameters'
                print 'Requires -p pid'
        else:
                streamModule.kill_p(args.pid, configs['lpath'])


else:
        print args.options, ': Command Not Found, check chirpy --help for the avaiable options'
        sys.exit()

