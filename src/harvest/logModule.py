import os
import datetime

#-------------------------------------------------------------------------

def chk_last(fpath):
        t = os.path.getmtime(fpath)
        t1 = datetime.datetime.fromtimestamp(t)
        t2 = datetime.datetime.now()
        td = t2 - t1
        s = td.total_seconds()
        return s

def ref_logs(lpath):
        logfiles = os.listdir(lpath)

        for f in logfiles:
                if chk_last(lpath+f) > 10:
                        os.remove(lpath+f)
	return

#--------------------------------------------------------------------------
