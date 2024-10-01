import sys
#import helper
import traceback
from pytwitter import Api
#import math
import praw #for reddit
#import requests
import datetime
import random
import os
import time
import pickle
import helper

#sleep_time = random.choice(range(7000))
#print('sleep time: ', sleep_time, flush=True)
#time.sleep(sleep_time)

print('num of arguments: ', len(sys.argv))
#print(sys.argv)
input_args = sys.argv

reddit = praw.Reddit(client_id=input_args[1], #REDDIT_CLIENT_ID
					 client_secret=input_args[2],#REDDIT_CLIENT_SECRET
					 password=input_args[3], #REDDIT_PASSWORD
					 user_agent=input_args[4], #REDDIT_USER_AGENT
					 username=input_args[5] #REDDIT_USER_NAME
					 )
twitter_api_authorized = Api(
		access_token=input_args[6], #TWITTER_ACCESS_TOKEN,
		access_secret=input_args[7], #TWITTER_ACCESS_TOKEN_SECRET
		client_id = '1814005222370672640',
		consumer_key = input_args[8], #TWITTER_CONSUMER_KEY
		consumer_secret = input_args[9], #TWITTER_CONSUMER_SECRET
	oauth_flow=True
	)

redgifs_submissions = [x.url for x in reddit.subreddit('MikeAdriano').top(time_filter='year',limit=10000) if ('redgifs' in x.url)] 
redgifs_submissions = redgifs_submissions + [x.url for x in reddit.subreddit('MikeAdriano').top(time_filter='month',limit=1000) if ('redgifs' in x.url)] 
print(len(redgifs_submissions))
#redgifs_submissions = redgifs_submissions + [x.url for x in reddit.subreddit('MikeAdriano').top(time_filter='day',limit=1000) if ('redgifs' in x.url)] 



filename = 'to_upload.mp4'
all_urls_ever = []
for x in range(0,50):
	print(x)
	if os.path.exists(filename):
		os.remove(filename)
	try:
		submission_url = random.choice(redgifs_submissions) #submission_url = ''
		while (not os.path.isfile(filename)) & (str(submission_url) not in all_urls_ever):
			video_url = helper.get_redgifs_embedded_video_url(redgifs_url=submission_url, output_fn=filename)
		print(submission_url)
		total_bytes = os.path.getsize(filename)
		print(total_bytes)
		resp = twitter_api_authorized.upload_media_chunked_init(
			total_bytes=total_bytes,
			media_type="video/mp4",
		)
		media_id = resp.media_id_string
		#print(media_id)

		segment_id = 0
		bytes_sent = 0
		file = open(filename, 'rb')
		idx=0
		while bytes_sent < total_bytes:
			chunk = file.read(4*1024*1024)
			status = twitter_api_authorized.upload_media_chunked_append(
					media_id=media_id,
					media=chunk,
					segment_index=idx
				)
			idx = idx+1
			
			bytes_sent = file.tell()
			#print(idx, media_id, status, bytes_sent)

		resp = twitter_api_authorized.upload_media_chunked_finalize(media_id=media_id)
		print(resp)


		time.sleep(5)
		resp = twitter_api_authorized.upload_media_chunked_status(media_id=media_id)
		print(resp)

		#tweet_title_final = helper.convert_hastag_to_at(tweet_title)

		twitter_api_authorized.create_tweet(
			media_media_ids=[media_id] #text=tweet_title_final,
		)

		#os.remove(filename)

		all_urls_ever.append(submission_url)
		print('pausing')
		time.sleep(600) #random.choice(range(7000))
	except Exception:
		print('error in flow')
		print(traceback.format_exc())
		continue
		
		

