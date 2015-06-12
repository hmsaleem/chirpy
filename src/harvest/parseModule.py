#!/usr/bin/python

import csv,codecs,cStringIO
import json
import operator
from prettytable import PrettyTable


#-------------------------------------------------------------------------------------------------------------

def tweet_info(json_obj):
        try:
                rtw = 'No'
                tweet = json.loads(json_obj)

                if 'retweeted_status' in tweet:
                        tweet = tweet['retweeted_status']
                        rtw = 'Yes'

                txt = tweet['text'].replace('\n', ' ').replace(',', ' ')
                htg = ''
                hashtag_list = tweet['entities']['hashtags']
                if (hashtag_list):
                        for hashtags in hashtag_list:
                                hashtag= hashtags['text'].lower()
                                if htg == '':
                                        htg = hashtag
                                else:
                                        htg = htg + ' '+hashtag

                username = tweet['user']['screen_name'].lower()
                tid = tweet['id_str']
                fwc = str(tweet['user']['followers_count'])
                cat = tweet['created_at'][4:-11]

                row = [tid, cat, username, txt, htg, fwc, rtw]
                row = [s.encode("utf-8") for s in row]

                return row

        except ValueError, err:
                return  False

#-------------------------------------------------------------------------------------------------------------

def create_csv(infile, outfile, query, uname):
	with open(infile, 'r') as fo:
		list_of_tweets = fo.readlines()

	tweet_dict = {}

	for tweetobject in list_of_tweets:
		x = tweet_info(tweetobject)
		x.append(1)
		if x:
			tid = x[0]
			if tid in tweet_dict:
				tweet_dict[tid][-1]+=1
			else:
				tweet_dict[tid] = x

	with open(outfile, 'wb') as fout:
		cwriter = csv.writer(fout, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

		title = ['tweet_id', 'created_on', 'username', 'tweet_txt', 'hashtag', 'followers', 'retweet', 'seen_count']
		cwriter.writerow(title)

		for item in tweet_dict:
			tweet_dict[item][-1] = str(tweet_dict[item][-1]).encode("utf-8")
			flag = 1

			if query:
				if query.lower() in tweet_dict[item][3].lower() or query.lower().replace('#', '') in tweet_dict[item][4]:
					pass
				else:
					flag = 0

			if uname:
				if uname.lower() == tweet_dict[item][2]:
					pass
				else:
					flag = 0
			if flag == 1:
				cwriter.writerow(tweet_dict[item])

	print outfile, 'Created'

	return

#-------------------------------------------------------------------------------------------------------------

def hash_list(infile, num):
	
	hashtag_lib ={}
	with open(infile, 'r') as fo:
		list_of_tweets = fo.readlines()

	count = 0

	for tweetobject in list_of_tweets:
		try:
			tweet = json.loads(tweetobject)
			hashtag_list = tweet['entities']['hashtags']
			if (hashtag_list):
				for hashtags in hashtag_list:
					hashtag= hashtags['text'].encode('UTF-8').lower()
					if hashtag in hashtag_lib:
						hashtag_lib[hashtag]+=1
					else:
						hashtag_lib[hashtag]=1

		except ValueError:
			count+=1

	sorted_hl = sorted(hashtag_lib.items(), key=operator.itemgetter(1), reverse=True)

	x = PrettyTable(["Hashtag", "Frequency"])
	x.align["Hashtag"] = "l"
	x.align["Frequency"] = "r"
	x.padding_width = 1

	for item, value in sorted_hl[:num]:
		x.add_row([item, value])

	print x

	return	
