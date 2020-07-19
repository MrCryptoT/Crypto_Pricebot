# encoding: utf-8

#Config area
CryptoSlugstoretrieve = 'bitcoin,ethereum,mimblewimblecoin,kava,chainlink,pivx' #can dynamically be expanded (within reason what can be displayed and Char limmit of Twitter)
convertto = 'USD' #Accepts Fiat and Crypto Slugs
slugorname = 'symbol'  #accepts 'slug' or 'name' or 'symbol'
seperatorstring = ' - ' #used for automated building of Output wihtout manual template use, whats between the cointicker and price
roundingto = 2 #how many decimals to display after price, useful for BTC display option
timebetweentweets = 43200 
emotionthreeshold = 15 #after what % should emojis change

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
#[coinname][2] represents its Slug
#[coinname][3] represents %  changed in 1 hour
#[coinname][4] represents %  changed in 24 hour 
#[coinname][5] represents the symbol
#[coinname][6] represents  a "chart up" or "chart down" Emoji to be filled in based on 24 hour change

#can be expanded with other params for the coins if needed

          response = session.get(url, params=parameters)
	  data = json.loads(response.text)
          
          i = 0
	  for dataset in data["data"]:
           #Get Coinname as set in Configuration (use this for display's/queries) 
	   coinnameinfo = str(data["data"][dataset][slugorname])
           extractedpricedata.append([coinnameinfo])

           #Get Coinprice (converted) 
           coinpricedata = str(round(data["data"][dataset]["quote"][convertto]["price"], roundingto))
	   extractedpricedata[i].append(coinpricedata)
           
           #Grab Slug
           coinslug = str(data["data"][dataset]["slug"])
           extractedpricedata[i].append(coinslug)

           #Grab % changed in 1 hour
           coinchange1hr = str(round(data["data"][dataset]["quote"][convertto]["percent_change_1h"], roundingto))
           extractedpricedata[i].append(coinchange1hr)

           #Grab % changed 24 hours
           coinchange24hr = str(round(data["data"][dataset]["quote"][convertto]["percent_change_24h"], roundingto))
           extractedpricedata[i].append(coinchange24hr)

           #Grab Symbol to identify Index in Array (and we hardcoded symbol in IF's)
           coinsymbol = str(data["data"][dataset]["symbol"])
           extractedpricedata[i].append(coinsymbol)
          
           if (data["data"][dataset]["quote"][convertto]["percent_change_24h"] > emotionthreeshold):
             extractedpricedata[i].append('📈🎉')
           elif (data["data"][dataset]["quote"][convertto]["percent_change_24h"] > 0):
             extractedpricedata[i].append('📈🤗')
           elif (data["data"][dataset]["quote"][convertto]["percent_change_24h"] < emotionthreeshold):
             extractedpricedata[i].append('📈😞')
           else:
             extractedpricedata[i].append('📉🙁')

           i += 1
	except (ConnectionError, Timeout, TooManyRedirects) as e:
	  print(e)
	return extractedpricedata

#main  


tmp = ''
api = get_api_access()
while True:
  pricedata  =  get_crypto_information()
#identify indexes of wanted coins for manual template
  i = 0
  for coin in pricedata:
    if pricedata[i][5] == 'BTC':
      btc = i
    if pricedata[i][5] == 'MWC':
      mwc = i
    if pricedata[i][5] == 'LINK':
      link = i
    if pricedata[i][5] == 'KAVA':
      kava = i
    if pricedata[i][5] == 'ETH':
      eth = i
    if pricedata[i][5] == 'PIVX':
      pivx = i
    i += 1

#Build our Output automatically - edit Twitter Message here for now
#  tmpstrbuilding = ''
#  for coin in pricedata:
#    tmpstrbuilding += str(coin[0]) + seperatorstring + str(coin[1]) + ' ' + convertto + ' 24Hr Change: ' + str(coin[4]) + str(coin[6]) + '\n'
#  twittertemplate for automatic building. Manual Template is below commented out (might need manual coding if new coins are added)
#  twittertemplate = 'Current HOT 🔥 Crypto Stats: 📉📈\n' \
#  + tmpstrbuilding \
#  +'\nSee you again after a ☕ in ' + str(timebetweentweets/60/60) +' hours!'

# Manual Template: 
  twittertemplate = 'Current HOT 🔥 Crypto prices:\n' \
  + 'BTC    ' + str(pricedata[btc][1]) + ' ' + convertto + ' 24Hr ' + str(pricedata[btc][4]) + '% ' + str(pricedata[btc][6]) + '\n' \
  + 'ETH    ' + str(pricedata[eth][1]) + ' ' + convertto + '  24Hr ' + str(pricedata[eth][4]) + '% ' + str(pricedata[eth][6]) + '\n' \
  + 'MWC  ' + str(pricedata[mwc][1]) + ' ' + convertto + '  24Hr ' + str(pricedata[mwc][4]) + '% ' + str(pricedata[mwc][6]) + '\n' \
  + 'LINK   ' + str(pricedata[link][1]) + ' ' + convertto + '    24Hr ' + str(pricedata[link][4]) + '% ' + str(pricedata[link][6]) + '\n' \
  + 'PIVX   ' + str(pricedata[pivx][1]) + ' ' + convertto + '   24Hr ' + str(pricedata[pivx][4]) + '% ' + str(pricedata[pivx][6]) + '\n' \
  + 'KAVA  ' + str(pricedata[kava][1]) + ' ' + convertto + '   24Hr ' + str(pricedata[kava][4]) + '% ' + str(pricedata[kava][6]) + '\n' \
  + '\nCYA after a ☕ in ' + str(timebetweentweets/60/60) + ' hours!'

#  api.update_status(status=twittertemplate)
  print(twittertemplate) #Debug print out of the Template message after Tweet
  time.sleep(timebetweentweets)
