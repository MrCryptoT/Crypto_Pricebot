# encoding: utf-8

#Config area

CryptoSlugstoretrieve = 'bitcoin,ethereum,mimblewimblecoin,compound,chainlink' #can dynamically be expanded (within reason what can be displayed and Char limmit of Twitter)
convertto = 'USD'
tmp = '' #Dont change
slugorname = 'symbol'  #accepts 'slug' or 'name' or 'symbol'
seperatorstring = '  -  ' #String coinname/slug and price are seperated by
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
#Build a 2 D Array as follows 
#extractedpricedata[0] represents the coinames as a List of Values (named depending on slugorname config value)
#extractedpricedata[coinname][0] represents the name (named depending on slugorname config value)
#extractedpricedata[coinname][1] represents the price
#can be expanded with other params for the coins if needed
	  extractedpricedata = []
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

  for coin in pricedata:
    shortest = 999
    longest = 0
    if (longest < len(coin[0])):
      longest =len(coin[0])
    if (shortest > len(coin[0])):
      shortest =len(coin[0])

  for coin in pricedata:
#Singeling out values would be rather simple if there is a need to mention just 1 crypto
#Automating seems a bit harder though since we can choose between symbols and slugs
#We could go overkill and grad slug,symbol and slug data to compare across all 3 - but honestly that's not worth the effort for now. 
#Rather "query" if coin[0] is the coin you expect f.E

# !!! This will break if Slug or name is chosen as display parameter in config section - would need to change here too
    if coin[0] == 'BTC':
      price_btc=str(coin[1])
    if coin[0] == 'MWC':
      price_mwc=str(coin[1])
    if coin[0] == 'LINK':
      price_link=str(coin[1])
    if coin[0] == 'COMP':
      price_comp=str(coin[1])
    if coin[0] == 'ETH':
      price_eth=str(coin[1])
#      print(price_btc)


#EXPERIMENTAL Formatting Fix
#get longest name and try to correct with spaces (2*spaces as missing chars as twitter has small spaces tabs sadly dont work)  longest = 0
    if (longest !=len(coin[0])):
      diff = longest - len(coin[0])
      prefix ='{:<' + str(diff*2+longest) + '}'
      padding =prefix.format(coin[0])
      coin[0] =padding

  tmpstrbuilding = ''
  for coin in pricedata:
    tmpstrbuilding += str(coin[0]) + seperatorstring + str(coin[1]) + ' ' + convertto + '\n'

#Build our Output - edit Twitter Message here for now
  twittertemplate = 'Current HOT 🔥 Crypto Stats: 📉📈\n' + tmpstrbuilding +'\nSee you again after a ☕ in ' + str(timebetweentweets/60/60) +' hours!'
#  api.update_status(status=twittertemplate)
  print(twittertemplate) #Debug print out of the Template message after Tweet
  time.sleep(timebetweentweets)
