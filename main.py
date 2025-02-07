import sys
#import helper
import traceback
from pytwitter import Api
import math
import praw #for reddit
#import requests
import datetime
import random
import os
import time
import pickle
import helper

sleep_time = random.choice(range(600))
print('sleep time: ', sleep_time, flush=True)
time.sleep(sleep_time)

print('num of arguments: ', len(sys.argv))
#print(sys.argv)
input_args = sys.argv

list_of_subreddits = ['Bukkake_Before_After',
					'bukkake',
					'ClassyPornstars',
					'ModelsGoneMild','blowbang',
					'Licked','porninfifteenseconds','Spittok','PressCUMference','MikeAdriano']
					#'nsfwcosplay''bigtitsinbikinis','tiktokthots','GirlsFinishingTheJob','BoutineLaModels',
					#'hentai','Futanari','FutanariGifs','futanari_Comics','FutanariHentai'] 
					#'BimboFetish','javdreams','deepthroat','ActuallyHugeCumshots','FemboyHentai',
					#,'BabeCock','CumCoveredSluts' #cumsluts,#SpitRoasted, Exxxtras HENTAI_GIF
					#,'Oilporn',Pornstar_moms, 'blowjobsandwich','xxxcaptions', 
					#'PornIsCheating','pornrelapsed',
star_subreddits = ['AngelaWhite','Miakhalifa','RileyReid','MiaMalkova','GabbieCarter','abelladanger',
				   'AdrianaChechik','LenaPaul','RemyLaCroix','Sashagrey','Eimi_Fukada','DreddxxxOnly',
				   'GiannaMichaels','BrandiLove','sophiedee','LisaAnn','JadaStevens', 'VioletMyers',
				   'KendraLust','valentinanappi','karleegrey','MandyMuse','Evalovia','AlettaOcean__',
				   'SaraJay','NicoletteSheaNew','KristyBlack','NatashaNice','KahoShibuya','SyrenDeMer',
				   'ClubDeeWilliams','ValericaSteele','chloe_cherry','GiaDerza_X','AshleyAdams', #'BriannaArson',
				   'KiannaDior','JasmineJaeXX','MarshaMay','BreeOlson','Alexis_Fawx',
				   'charlottesartre','SophiaLockeX','AvaDevine','ArabelleRaphaelFans',
				   'AshleyAdams','KenzieReeves','SkylarVox','LexiLuna','LaurenPhillips','ElizaIbarra',
				   'AngelWickyX','lasirena69','liz_103','RoseMonroe','VeronicaLeal','ConniePerignon_',
				   'NikkiBenz','JewelzBlu','NicoleDoshi','KarmaRx','IndicaFlower','eva_angelina','SukiSin',
				   'AnnaBellPeaks','AnnaDeVille','SarahVandella','AmyAnderssen','Ashlynn_Brooke','BonnieRotten',
				   'Cali_Carter','BrooklynChase','ChristyMack','EvaNotty','JaydenJaymes','JosephineJackson',
				   'Katsumi','priyarai','SavannahBond','lanarhoades','AvaAddams','GinaValentina','KelsiMonroe',
				   'StephanieMichelle']
				   
all_subreddits = list_of_subreddits+star_subreddits

reddit = praw.Reddit(client_id=input_args[1], #REDDIT_CLIENT_ID
					 client_secret=input_args[2],#REDDIT_CLIENT_SECRET
					 password=input_args[3], #REDDIT_PASSWORD
					 user_agent=input_args[4], #REDDIT_USER_AGENT
					 username=input_args[5] #REDDIT_USER_NAME
					 )
twitter_api_authorized = Api(
		access_token=input_args[6], #TWITTER_ACCESS_TOKEN_BL,
		access_secret=input_args[7], #TWITTER_ACCESS_TOKEN_SECRET_BL
		client_id = '1712104648881192960',
		consumer_key = input_args[8], #TWITTER_CONSUMER_KEY
		consumer_secret = input_args[9], #TWITTER_CONSUMER_SECRET
	oauth_flow=True
	)
#red_gifs_api = redgifsAPI() #redgifs.API()
#time.sleep(2)
#red_gifs_api.login()
today_str = str(datetime.datetime.now().date())
tommorrow_str = str(datetime.date.today() + datetime.timedelta(days=1))

try:
	with open ('todays_list.ob', 'rb') as fp:
		todays_alreadysent_list = pickle.load(fp)
		#print(todays_alreadysent_list)
except:
	print('Creating new todays_list list')
	todays_alreadysent_list = []
if today_str in todays_alreadysent_list:
	pass
else:
	todays_alreadysent_list = [today_str]#, tommorrow_str]
try:
	with open ('all_titles_ever.ob', 'rb') as fp:
		all_titles_ever = pickle.load(fp)
		#print(todays_alreadysent_list)
except:
	print('Creating new all_titles_ever list')
	all_titles_ever = []

filename = 'to_upload.mp4'

while not os.path.isfile(filename):
	subreddits_to_choose_from = [x for x in all_subreddits if x not in todays_alreadysent_list]
	subreddit = random.choice(subreddits_to_choose_from)
	print(subreddit)
	for x in reddit.subreddit(subreddit).top(time_filter='day',limit=25):
		#print(x.url)
		if ('redgifs' in x.url) & (str(x.title) not in all_titles_ever):
			url = x.url
			print(url, flush=True)
			video_url = helper.get_redgifs_embedded_video_url(redgifs_url=url,output_fn=filename)
			#print(tweet_title, flush=True)
			break
		elif ('redgifs' in x.url) & (str(x.title) in todays_alreadysent_list):
			print('title already in sent list')
	original_title = str(x.title)
	#tweet_title=original_title.replace(' my ',' the ').replace(' I ',' they ').replace("I'm","they're") \
	#					.replace("I've","they've").replace("I'd","they'd").replace(' me ',' them ').replace(' Me ',' Them ')
	tweet_title = original_title
	if subreddit in star_subreddits:
		hastag_modified = str(subreddit).replace('_','').replace('X','') \
			.replace('Club','').replace('New','').replace('Fans','').replace('xxxOnly','') \
			.replace('2','').replace('[OC]','').replace('[oc]','').replace('(OC)','')
		tweet_title = tweet_title + ' #' + hastag_modified
		'''hastag_with_space = ''
		for i, letter in enumerate(hastag_modified):
		    if i and letter.isupper():
		        hastag_with_space += ' '
		        hastag_with_space += letter
		if hastag_with_space in tweet_title:
			tweet_title = tweet_title.replace(hastag_with_space, '#'+hastag_modified)
		else:
			tweet_title = tweet_title + ' #' + hastag_modified'''
todays_alreadysent_list.append(subreddit)
todays_alreadysent_list.append(str(x.title))
with open('todays_list.ob', 'wb') as fp:
	#pickle.dump([], fp)
	pickle.dump(todays_alreadysent_list, fp)


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
	print(idx, media_id, status, bytes_sent)

resp = twitter_api_authorized.upload_media_chunked_finalize(media_id=media_id)
print(resp)


time.sleep(10)
resp = twitter_api_authorized.upload_media_chunked_status(media_id=media_id)
print(resp)

tweet_title_final = helper.convert_hastag_to_at(tweet_title).split('#')[0]

twitter_api_authorized.create_tweet(
	text=tweet_title_final,
	media_media_ids=[media_id]
)

os.remove(filename)

all_titles_ever.append(str(original_title))
with open('all_titles_ever.ob', 'wb') as fp:
	#pickle.dump([], fp)
	pickle.dump(all_titles_ever, fp)

