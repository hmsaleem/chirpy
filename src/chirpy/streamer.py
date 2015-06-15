#'''
#author = Saleem
#twitterstreamer is a tool that actively listens to live Twitter stream for keyword mentions.
#'''
#-------------------------------------------------------------------------------------------------------------

import os
import sys
import codecs

if sys.stdout.encoding == None:
    os.putenv("PYTHONIOENCODING", 'UTF-8')
    os.execv(sys.executable, ['python']+sys.argv)

sys.dont_write_bytecode = True

#-------------------------------------------------------------------------------------------------------------

from optparse import OptionParser
from datetime import datetime
import helpModule
import profileModule
import time
import multiprocessing
from configModule import read_config
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

parser = OptionParser()
parser.add_option("-o", "--op", help = "output dir", type = "string", dest = "output_dir")
parser.add_option("-d", "--dy", help = "number of days", type = "string", dest = "days")
parser.add_option("-f", "--of", help = "path to output file", type = "string", dest = "output_file")
parser.add_option("-k", "--kw", help = "list of query words", type = "string", dest = "query")
(options, args) = parser.parse_args()

#-------------------------------------------------------------------------------------------------------------

def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

#-------------------------------------------------------------------------------------------------------------

output_dir = options.output_dir
days = options.days
output_file = options.output_file
query = options.query

configs = read_config()
ppath = configs['ppath']
lpath = configs['lpath']
root = configs['dpath']
if root == 'False':
	root = './'

outfile = root + output_dir + '/' + output_file

fo = open(outfile, 'w')
fo.close()

parentid = str(os.getpid())
logfile = lpath+parentid+'.streamlog'

helpModule.make_outdir(root+output_dir)

profile = profileModule.get_profile(ppath, lpath)
profilepath = ppath+profile+'.profile'
deets = profileModule.get_deets(profilepath)

#-------------------------------------------------------------------------------------------------------------

class StdOutListener(StreamListener):

    def on_data(self, data):
        if  'in_reply_to_status' in data:
		with open(outfile,'a') as tf:
            		tf.write(data)
        return True

    def on_error(self, status):
        pass
	return True

#-------------------------------------------------------------------------------------------------------------

def strmlister():
	listner = StdOutListener()
	
	auth = OAuthHandler(deets["consumer_key"], deets["consumer_secret"])
	auth.set_access_token(deets["access_token"], deets["access_token_secret"])
	stream = Stream(auth, listner)

	trackkwrds = query.split(',')
	#trackkwrds = [x.decode("utf-8") for x in trackkwrds]
	
	stream.filter(track=trackkwrds)

#-------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

	p = multiprocessing.Process(target=strmlister)
	p.start()

	start_time = datetime.now()	

	childid = p.pid

	with open(logfile, 'a') as lfo:
		lfo.write(profile+'\n')
		lfo.write(query+'\n')
		lfo.write(str(childid)+'\n')	

	runtime = int(days)*10*60*24
	#runtime = int(days)*10

	for i in xrange(runtime):
		if not 	check_pid(childid):
			os.remove(logfile)
			os.system('kill %d' % os.getpid())

                if os.path.isfile(outfile):
                        num_lines = str(sum(1 for line in open(outfile)))
                else:
                        num_lines = str(0)
                etime = str(datetime.now() - start_time)[:-7]
                with open(logfile, 'a') as lfo:
                        lfo.write(etime+' '+num_lines+'\n')
                time.sleep(6)

		
	p.terminate()
	os.remove(logfile)
	p.join()

