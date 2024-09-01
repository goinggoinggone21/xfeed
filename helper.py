import requests
import datetime
import random


import requests, traceback, json, io, os, urllib.request, sys
#sys.stdout.reconfigure(encoding='utf-8')


def get_redgifs_embedded_video_url(redgifs_url, output_fn):
	API_URL_REDGIFS = 'https://api.redgifs.com/v2/gifs/'
	r = requests.get('https://api.redgifs.com/v2/auth/temporary')
	token = r.json()['token']

	headers={"Authorization": "Bearer "+token}
	try:
		print("redgifs_url = {}".format(redgifs_url))

		#Get RedGifs video ID
		redgifs_ID = redgifs_url.split('/watch/', 1)
		redgifs_ID = redgifs_ID[1]
		print("redgifs_ID = {}".format(redgifs_ID))
		
		sess = requests.Session()
		
		#Get RedGifs Video Meta
		# request = requests.get(API_URL_REDGIFS + redgifs_ID)
		request = sess.get(API_URL_REDGIFS + redgifs_ID, headers=headers)
		print(request)
		
		if request is None:
			return
		else:
			rawData = request.json()
			#print(rawData)
			#print("rawData = {}".format(rawData))

			#Get HD video url
			hd_video_url = rawData['gif']['urls']['hd']
			#print("hd_video_url = {}".format(hd_video_url))
			
			with sess.get(hd_video_url, stream=True) as r:
				with open(output_fn, 'wb') as f:
					for chunk in r.iter_content(chunk_size=8192): 
						# If you have chunk encoded response uncomment 
						# if and set chunk_size parameter to None.
						# if chunk: 
						f.write(chunk)

			return hd_video_url
	except Exception:
		traceback.print_exc()
		return
def convert_hastag_to_at(tweet_title_):
	if '#AngelWicky' in   tweet_title_:
		return  tweet_title_.replace('#AngelWicky','@Angel_Wicky_II')
	elif '#SukiSin' in tweet_title_:
		return tweet_title_.replace('#SukiSin','@sukisinxx')
	elif '#liz_103' in tweet_title_:
		return tweet_title_.replace('#liz_103','@LilyLouOfficial')
	elif '#JosephineJackson' in tweet_title_:
		return tweet_title_.replace('#JosephineJackson','@josephinejxxx')
	elif '#SophiaLocke' in tweet_title_:
		return tweet_title_.replace('#SophiaLocke','@_SophiaLocke_')
	elif '#ArabelleRaphael' in tweet_title_:
		return tweet_title_.replace('#ArabelleRaphael','@MommyArabelle')
	elif '#VeronicaLeal' in tweet_title_:
		return tweet_title_.replace('#VeronicaLeal','@VeronicaLealoff')
	elif '#ValericaSteele' in tweet_title_:
		return tweet_title_.replace('#ValericaSteele','@VALERiCAx')
	elif '#AnnaDeVille' in tweet_title_:
		return tweet_title_.replace('#AnnaDeVille','@AnnadeVilleXXX')
	elif '#VioletMyers' in tweet_title_:
		return tweet_title_.replace('#VioletMyers','@violetsaucy')
	elif '#KiannaDior' in tweet_title_:
		return tweet_title_.replace('#KiannaDior','@Kianna_Dior')
	elif '#AvaDevine' in tweet_title_:
		return tweet_title_.replace('#AvaDevine','@1avadevine')
	elif '#RemyLaCroix' in tweet_title_:
		return tweet_title_.replace('#RemyLaCroix','@RemyLaCroixxxxx')
	elif '#StephanieMichelle' in tweet_title_:
		return tweet_title_.replace('#StephanieMichelle','@omystephanie')
	elif '#MandyMuse' in tweet_title_:
		return tweet_title_.replace('#MandyMuse','@MandyMuse69')
	elif '#KendraLust' in tweet_title_:
		return tweet_title_.replace('#KendraLust','@KendraLust')
	elif '#SyrenDeMer' in tweet_title_:
		return tweet_title_.replace('#SyrenDeMer','@SyrenDeMerXXX')
	elif '#AshleyAdams' in tweet_title_:
		return tweet_title_.replace('#AshleyAdams','@xoxoashleyadams')
	elif '#KristyBlack' in tweet_title_:
		return tweet_title_.replace('#KristyBlack','@KristyBlack_new')
	elif '#ConniePerignon' in tweet_title_:
		return tweet_title_.replace('#ConniePerignon','@connperignon')
	elif '#evaangelina' in tweet_title_:
		return tweet_title_.replace('#evaangelina','@onlyevaangelina')
	elif '#NatashaNice' in tweet_title_:
		return tweet_title_.replace('#NatashaNice','@BeNiceNatasha \n \n https://onlyfans.com/benicenatasha')
	else:
		return tweet_title_

