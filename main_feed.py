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

imojis_list = ['🥰','😍','🤩','🫣','🥵','🥹','❤️‍🔥','🫶','👀','🫦','🔥','✨','💖']
heart_imojis = ['❤️','💙','💚','💛','💜','💟','🖤','♥️','🧡','🤍','🤎','💦']
def get_tweet_title(reddit_title):
    try:
        reddit_title_clean = reddit_title.replace('[Discussion]','').replace('[Pick]','')
        #print('reddit_title_clean ', reddit_title_clean)
        brackets = reddit_title_clean.split('[')[1].split(']')[0]
        #print('brackets ',brackets)
        final_twitter_title = brackets.title() + ' ' + random.choice(imojis_list)
        #print(final_twitter_title)
        return final_twitter_title
    except:
        print('No Brackets')
        final_twitter_title = random.choice(heart_imojis)*3
        #print(final_twitter_title)
        return final_twitter_title
        pass


#print('num of arguments: ', len(sys.argv))
#print(sys.argv)

input_args = sys.argv

reddit = praw.Reddit(client_id=str(input_args[1]), #REDDIT_CLIENT_ID
					 client_secret=str(input_args[2]),#REDDIT_CLIENT_SECRET
					 password=str(input_args[3]), #REDDIT_PASSWORD
					 user_agent=str(input_args[4]), #REDDIT_USER_AGENT
					 username=str(input_args[5]) #REDDIT_USER_NAME
					 )
twitter_api_authorized = Api(
		access_token=input_args[6], #TWITTER_ACCESS_TOKEN,
		access_secret=input_args[7], #TWITTER_ACCESS_TOKEN_SECRET
		client_id = '1861172154123067392',
		consumer_key = input_args[8], #TWITTER_CONSUMER_KEY
		consumer_secret = input_args[9], #TWITTER_CONSUMER_SECRET
	oauth_flow=True
	)

#Load all list to remove duplicates
try:
	with open ('all_urls_ever.ob', 'rb') as fp:
		all_urls_ever = pickle.load(fp)
		#print(todays_alreadysent_list)
except:
	all_urls_ever = []


#Load Reddits
reddits_with_redgif = [x for x in reddit.subreddit('MikeAdriano').top(time_filter='year',limit=1000) if ('redgifs' in x.url)]
reddits_with_redgif = reddits_with_redgif + [x for x in reddit.subreddit('MikeAdriano').top(time_filter='month',limit=1000) if ('redgifs' in x.url)]
reddits_with_redgif = reddits_with_redgif + [x for x in reddit.subreddit('MikeAdriano').top(time_filter='all',limit=1000) if ('redgifs' in x.url)]
print('population: ', len(reddits_with_redgif))

for reddit_submission in reddits_with_redgif:
	random_index_selection = random.randint(0,len(reddits_with_redgif)-1)
	submission_url = reddits_with_redgif[random_index_selection].url
	submission_title = reddits_with_redgif[random_index_selection].title
	if (str(submission_url) not in all_urls_ever):
		break
	else:
		continue

tweet_title_final = get_tweet_title(submission_title)
print('submission_url: ', submission_url)
print('submission_title: ', submission_title)
print('tweet_title_final: ', tweet_title_final)

filename = 'to_upload.mp4'
if os.path.exists(filename):
    os.remove(filename)

try:
    #while (not os.path.isfile(filename)) & (str(submission_url) not in all_urls_ever):
    video_url = helper.get_redgifs_embedded_video_url(redgifs_url=submission_url, output_fn=filename)
    total_bytes = os.path.getsize(filename)
    print('total_bytes: ', total_bytes)
    if int(total_bytes) < 1000000:
        print('File Size Too Small')
        with open('all_urls_ever.ob', 'wb') as fp:
            #pickle.dump([], fp)
            pickle.dump(all_urls_ever, fp)
        #continue
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

    twitter_api_authorized.create_tweet(
        media_media_ids=[media_id], 
        text=tweet_title_final
    )

    os.remove(filename)

    all_urls_ever.append(submission_url)
    with open('all_urls_ever.ob', 'wb') as fp:
        #pickle.dump([], fp)
        pickle.dump(all_urls_ever, fp)
    if os.path.exists(filename):
        os.remove(filename)
    #print('pausing')
    #time.sleep(600) #random.choice(range(7000))
except Exception:
    print('error in flow')
    print(traceback.format_exc())
    pass
    #continue


		
		

