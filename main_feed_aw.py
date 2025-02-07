import sys
#import helper
import traceback
from pytwitter import Api
#import math
import praw #for reddit
import requests
import datetime
import random
import os
import time
import pickle
import helper

#sleep_time = random.choice(range(7000))
#print('sleep time: ', sleep_time, flush=True)
#time.sleep(sleep_time)

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
		client_id = '1829777330430230530',
		consumer_key = input_args[8], #TWITTER_CONSUMER_KEY
		consumer_secret = input_args[9], #TWITTER_CONSUMER_SECRET
	oauth_flow=True
	)

#Load all list to remove duplicates
try:
    with open ('all_aw_urls_ever.ob', 'rb') as fp:
        all_aw_urls_ever = pickle.load(fp)
        #print(todays_alreadysent_list)
except:
    all_aw_urls_ever = []

def check_substrings(string, substrings):
  return any(sub in string for sub in substrings)
def find_images_in_reddit(subreddit, search):
    list_of_urls = []
    for x in reddit.subreddit(subreddit).search(search, time_filter='all'):
        #print(x.url)
        if any(sub in x.url for sub in ['jpg','png','jpeg']) & (not x.over_18):
            #print(x.title)
            #print(x.url)
            list_of_urls.append(x.url)
        elif 'gallery' in x.url:
            try:
                for media in x.media_metadata.values():
                    if media["e"] == "Image":
                        list_of_urls.append(media["s"]["u"])
            except:
                continue
    return list_of_urls
#list_test = find_images_in_reddit('ClassyPornstars','Angela White')
#print(list_test)


#Load Reddits
list_of_subreddits = ['ModelsGoneMild','gentlemanboners',
'PrettyGirls','BeautifulFemales','ClassyPornstars','FamousFaces',
'Nicegirls','SFWcurvy','selfies','trueratecelebrities',
'celebrities']#'AngelaWhite','PornStarHQ','porn']#,'slutwear']
#list_of_subreddits=['all']
urls_with_aw_pic = []
for sub_red in list_of_subreddits:
    #print(sub_red)
    list_test = find_images_in_reddit(sub_red,'Angela White')
    #list_test2 = find_images_in_reddit(sub_red,'AngelaWhite')
    #print(len(list_test))
    urls_with_aw_pic.extend(list_test)
aw_pic_urls_to_choose_from = [x for x in urls_with_aw_pic if x not in all_aw_urls_ever]
print('Pics to choose from: ', len(set(aw_pic_urls_to_choose_from)))


url_to_upload = random.choice(aw_pic_urls_to_choose_from)

fn_format = url_to_upload.split('.')[-1]
fn_to_upload = 'to_upload.{}'.format(fn_format)
print('url to upload: ',url_to_upload)
r = requests.get(url_to_upload)
with open(fn_to_upload,"wb") as f:
    f.write(r.content)

try:
    total_bytes = os.path.getsize(fn_to_upload)
    print(total_bytes)

    resp = twitter_api_authorized.upload_media_chunked_init(
        total_bytes=total_bytes,
        media_type="image/"+fn_format,
    )
    media_id = resp.media_id_string
    #print(media_id)

    segment_id = 0
    bytes_sent = 0
    file = open(fn_to_upload, 'rb')
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
        print(idx, media_id, status, bytes_sent)

    resp = twitter_api_authorized.upload_media_chunked_finalize(media_id=media_id)
    print(resp)


    time.sleep(10)
    #resp = api_authorized.upload_media_chunked_status(media_id=media_id)
    #print(resp)

    #tweet_text_final = helper.convert_hastag_to_at(original_title)


    twitter_api_authorized.create_tweet(
    #   text=tweet_text_final,
        media_media_ids=[media_id]
    )


    os.remove(fn_to_upload)

    all_aw_urls_ever.append(url_to_upload)
    with open('all_aw_urls_ever.ob', 'wb') as fp:
        #pickle.dump([], fp)
        pickle.dump(all_aw_urls_ever, fp)
    if os.path.exists(fn_to_upload):
        os.remove(fn_to_upload)
    #print('pausing')
    #time.sleep(600) #random.choice(range(7000))
except Exception:
    print('error in flow')
    print(traceback.format_exc())
    pass
    #continue


		
		

