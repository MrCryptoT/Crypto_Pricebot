# encoding: utf-8

#Config area

CryptoSlugstoretrieve = 'bitcoin,ethereum,mimblewimblecoin,compound,chainlink' #can dynamically be expanded (within reason what can be displayed and Char limmit of Twitter)
convertto = 'USD'
tmp = ''
slugorname = 'symbol'  #accepts 'slug' or 'name' or 'symbol'
seperatorstring = '  -  '
timebetweentweets = 28800 #in seconds 

#CMC API Key 
CMC_API_KEY_freeplan = 'Replace me!'

#Twitter API Region
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

#Build a 2 D Array as follows 
#[0] represents the coinames (slugorname config option)
#[coinname][0] represents the name 
#[coinname][1] represents the price
#can be expanded with other params for the coins if needed

          response = session.get(url, params=parameters)
	  data = json.loads(response.text)
          i = 0
	  for dataset in data["data"]:
	   coinnameinfo = str(data["data"][dataset][slugorname])
           extractedpricedata.append([coinnameinfo])

           coinpricedata = str(round(data["data"][dataset]["quote"][convertto]["price"], 2))
	   extractedpricedata[i].append(coinpricedata) 
           i += 1


	except (ConnectionError, Timeout, TooManyRedirects) as e:

	  print(e)

	return extractedpricedata
  
#main  

#Actuall tweet area - fire a tweet 
api = get_api_access()
while True:

  pricedata  =  get_crypto_information()

#First, Clean the Output for Twitter
#Sadly spaces are too small to autofill to the longest comon string, we need double the amount of spaces of missing chars

#EXPERIMENTAL
#get longest name and try to correct with spaces (2*spaces as missing chars as twitter has small spaces tabs sadly dont work)
  longest = 0
  shortest = 999
  for coin in pricedata:
    if (longest < len(coin[0])):
      longest =len(coin[0])
    if (shortest > len(coin[0])):
      shortest =len(coin[0])

  for coin in pricedata:
    if (longest !=len(coin[0])):
      diff = longest - len(coin[0])
      prefix ='{:<' + str(diff*2+longest) + '}'
      padding =prefix.format(coin[0])
      coin[0] =padding


#Build our Output - edit Twitter Message here for now 
  tmpstrbuilding = ''
  for coin in pricedata:

    tmpstrbuilding += str(coin[0]) + seperatorstring + str(coin[1]) + ' ' + convertto + '\n'

#  print(tmpstrbuilding)
  twittertemplate = 'Current HOT 🔥 Crypto Stats: 📉📈\n' + tmpstrbuilding +'\nSee you again after a ☕ in ' + str(timebetweentweets/60/60) +' hours!'
#  api.update_status(status=twittertemplate)
  print(twittertemplate) #Debug print out of the Template message after Tweet
  time.sleep(timebetweentweets)
