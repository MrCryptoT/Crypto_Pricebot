# encoding: utf-8

#Todo's: 
# - Number of Dataproviders should be in the 2D Array (stored per coin slug) 
# - Calc of price needs to respect above Values
# - User needs to be informed if not all choosen datasources are availlable
# - Build a "Stringarray" of "[coinname][1]" with availlable price data. 
# Unpack the Stringified array and divide by total number of Items in the list. 
# this is an easy way to ensure price Calcs are actually correct.

#Config area
CryptoSlugstoretrieve = 'bitcoin,ethereum,mimblewimblecoin,kava,chainlink,pivx' #can dynamically be expanded (within reason what can be displayed and Char limmit of Twitter)
convertto = 'USD' #Accepts Fiat and Crypto Slugs
slugorname = 'symbol'  #accepts 'slug' or 'name' or 'symbol'
seperatorstring = ' - ' #used for automated building of Output wihtout manual template use, whats between the cointicker and price
roundingto = 2 #how many decimals to display after price, useful for BTC display option
timebetweentweets = 43200 
emotionthreeshold = 10 #after what % should emojis change
Totaldatasources = 1 #We always use CMC as a "master" for now
coingeckoenabled = True #accepts True or False 
if (coingeckoenabled) Totaldatasources += 1




debug = False
emojiup = '📈🤗'
emojidown = '📉😞'
emojiupalot = '📈🎉'
emojidownalot = '📉🙁'
currencysymbol = '$' #Symbol to use infront of Crypto Symbol - leave Empty if you display the name or Slug. (Only in manual Tmp$

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
def strtolst(srcstr):
        outputlist = srcstr.split(',')
        return outputlist
def lsttostr(srclst):
        outputstring = ''
        for str in srclist:
          outputstring += str + ','
        #remove last delimiter comma
        outputstring = outputstring[:-1]
        return outputstring
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
             extractedpricedata[i].append(emojiupalot)
           elif (data["data"][dataset]["quote"][convertto]["percent_change_24h"] > 0):
             extractedpricedata[i].append(emojiup)
           elif (data["data"][dataset]["quote"][convertto]["percent_change_24h"] < emotionthreeshold*-1):
             extractedpricedata[i].append(emojidownalot)
           else:
             extractedpricedata[i].append(emojidown)

           i += 1
	except (ConnectionError, Timeout, TooManyRedirects) as e:
	  print(e)

#Coingecko Area - figure out how to "choose" data providers at some point. (what if a provider doesnt have the data?) 
      
        if (coingeckoenabled):

          for coin in strtolst(CryptoSlugstoretrieve):

            url = 'https://api.coingecko.com/api/v3/coins/' + coin + '?localization=false'
            headers = {
              'accept': 'application/json',
            }
            session = Session()
            session.headers.update(headers)
            try:
              response = session.get(url, params=parameters)
              data = json.loads(response.text)
              #Get Coinname as set in Configuration (use this for display's/queries) 
              if (slugorname == 'slug'):
                coinnameinfo = str(data['id'])
              elif (slugorname == 'name'):
                coinnameinfo = str(data['id'])
              else:
                coinnameinfo = str(data[slugorname])
             #Get Coinprice (converted) 
              coinpricedata = round(data["market_data"]["current_price"][convertto.lower()], roundingto)
             #Grab Slug
              coinslug = str(data["id"])
             #Grab % changed in 1 hour

              coinchange1hr = str('?')
             #Grab % changed 24 hour
              coinchange24hr =round(data["market_data"]["price_change_percentage_24h"], roundingto)
              coinsymbol = str(data["symbol"])
              
              ii = 0
              for coin in extractedpricedata:
                if extractedpricedata[ii][5].strip() == coinsymbol.upper().strip():
                  if (debug):
                    print('before:' + extractedpricedata[ii][1])
                  extractedpricedata[ii][1] = extractedpricedata[ii][1] + "," + round(coinpricedata, roundingto)
                  
#Not existent on Coingecko           extractedpricedata[i][3] = ((coinchange1hr + extractedpricedatacoingecko[i][3]) /2)
                  extractedpricedata[ii][4] = round(((coinchange24hr + float(extractedpricedata[ii][4])) /2), roundingto)
                  if (debug):
                    print('after:' + str(extractedpricedata[ii][1]))
                  if (extractedpricedata[ii][4] > emotionthreeshold):
                    extractedpricedata[ii][6] = (emojiupalot) 
                  elif (extractedpricedata[ii][4] > 0):
                    extractedpricedata[ii][6] = (emojiup)
                  elif (extractedpricedata[ii][4] < emotionthreeshold*-1):
                    extractedpricedata[ii][6] = (emojidownalot)
                  else:
                    extractedpricedata[ii][6] = (emojidown)

                ii += 1
            except (ConnectionError, Timeout, TooManyRedirects) as e:
              print(e)



#Round Price according to availlable Datapoints.


      
        try:
            i = 0
            ii = 0
            for coin in extractedpricedata:
                ctr = 0
                for dataset in strtolst(extractedpricedata[ii][4]):
                ctr += dataset
                i += 1
                if i = strtolst(extractedpricedata[ii][4]).count
                   extractedpricedata[ii][4] = ctr / i
             ii += 1
            ctr = 0 #reset CTR after calc
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)      
   


	return extractedpricedata
#End Getdata Function

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
  + currencysymbol + 'BTC   ' + str(pricedata[btc][1]) + ' ' + convertto + ' 24Hr ' + str(pricedata[btc][4]) + '% ' + str(pricedata[btc][5]) + '\n' \
  + currencysymbol + 'ETH   ' + str(pricedata[eth][1]) + ' ' + convertto + '  24Hr ' + str(pricedata[eth][4]) + '% ' + str(pricedata[btc][5]) + '\n' \
  + currencysymbol + 'MWC ' + str(pricedata[mwc][1]) + ' ' + convertto + '    24Hr ' + str(pricedata[mwc][4]) + '% ' + str(pricedata[btc][5]) + '\n' \
  + currencysymbol + 'LINK  ' + str(pricedata[link][1]) + ' ' + convertto + '      24Hr  ' + str(pricedata[link][4]) + '% ' + str(pricedata[btc][5]) + '\n' \
  + currencysymbol + 'PIVX  ' + str(pricedata[pivx][1]) + ' ' + convertto + '     24Hr   ' + str(pricedata[pivx][4]) + '% ' + str(pricedata[btc][5]) + '\n' \
  + currencysymbol + 'KAVA ' + str(pricedata[kava][1]) + ' ' + convertto + '    24Hr   ' + str(pricedata[kava][4]) + '% ' + str(pricedata[btc][5]) + '\n' \
  + '\nCYA after a ☕ in ' + str(timebetweentweets/60/60) + ' hours!'

#  api.update_status(status=twittertemplate)
  print(twittertemplate) #Debug print out of the Template message after Tweet
  time.sleep(timebetweentweets)
