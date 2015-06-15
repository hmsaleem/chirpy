'''
@uthor: Haji Mohammad Saleem

Helper module for Harvest
'''

import os, json
import errno
import time

#------------------------------------------------------------------------

def write_to_file(jsonlist, filepath):
        with open(filepath, 'a') as fo:
                for item in jsonlist:
                        fo.write(json.dumps(item))
                        fo.write('\n')
        return

def make_outdir(path):
        try:
                os.makedirs(path)
        	print 'Output Directory Created'
		time.sleep(0.5)
	except OSError as exception:
                if exception.errno != errno.EEXIST:
                        raise
