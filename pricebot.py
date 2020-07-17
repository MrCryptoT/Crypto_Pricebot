# encoding: utf-8

#Config area

CryptoSlugstoretrieve = 'bitcoin,ethereum,mimblewimblecoin,compound,chainlink' #can dynamically be expanded (within reason what can be displayed and Char limmit of Twitter)
convertto = 'USD'
extractedpricedata = []
tmp = ''
slugorname = 'symbol'  #accepts 'slug' or 'name' or 'symbol'
seperatorstring = ' = '
timebetweentweets = 14400 #in seconds 

#CMC API Key 
CMC_API_KEY_freeplan = 'Replace me!'

#Twitter API Region
consumer_key = "Replace me!"
consumer_secret = "Replace me!"

access_token = "Replace me!"
access_token_secret = "Replace me!"

#imports

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import tweepy

#functions
def get_api_access():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	return tweepy.API(auth)


def get_crypto_information():
#CMC API Area
	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
	parameters = {
	  'slug':CryptoSlugstoretrieve,
	  'convert':convertto
	}
	headers = {
	  'Accepts': 'application/json',
	  'X-CMC_PRO_API_KEY': CMC_API_KEY_freeplan,
	}

	session = Session()
	session.headers.update(headers)

	try:
	  extractedpricedata = []
	  response = session.get(url, params=parameters)
	  data = json.loads(response.text)
	  for dataset in data["data"]:
	   tmp = str(data["data"][dataset][slugorname])
	   tmp += seperatorstring
	   tmp += str(data["data"][dataset]["quote"][convertto]["price"])
	#Add to global array
	   extractedpricedata.append(tmp)

	except (ConnectionError, Timeout, TooManyRedirects) as e:

	  print(e)

	return extractedpricedata    
  
#main  

#Actuall tweet area - fire a tweet 
api = get_api_access()
while True:

  pricedata =  get_crypto_information()
  tmpstrbuilding = ''
  for coininfo in pricedata: 
    tmpstrbuilding += coininfo + ' ' + convertto + '\n'

  twittertemplate = 'Current HOT 🔥 Crypto Stats: 📉📈\n' + tmpstrbuilding +'\n\nSee you again in ' + str(timebetweentweets/60/60) +' hours!'
  api.update_status(status=twittertemplate)
  print(twittertemplate) #Debug print out of the Template message after Tweet
  time.sleep(timebetweentweets)
