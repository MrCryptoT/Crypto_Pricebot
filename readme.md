A simple version of a Twitter bot checking CMC Market Data to return requested Coin's prices. 

The list of Coins to retrieve is dynamic, and it will list everything accordingly after changing ``CryptoSlugstoretrieve``̀ just make sure to enter the Coin's Slug's seperated by ","!

This is a minimalistic implementation for a Bot that does 1 simple lookup and an according Post. 
This can be heavily expanded upon, for example by supplying an "easy" way to create a templatefile externally for easy edits, currently this template needs to be edited "in script" 

Also I'm sure there are some edge cases I ignored for now => <br>
f.E what happens if a twitter message is longer than twitters char limmit? <br>
What if CMC API Limit is reached?<br>
How many requests will that take etc...

**This Software is to take "as is"** 

**Setup**
 - ``sudo apt-get install python-pip python-py``̀
 - ``pip install git+https://github.com/tweepy/tweepy.git``̀
 - Create API Key's for twitter on the Dev Portal https://developer.twitter.com/en/portal
 - Create API Key on CMC https://developer.twitter.com/en/portal
 - ``sudo git clone git@github.com:MrCryptoT/Crypto_Pricebot.git``̀
 - ``cd Crypto_Pricebot``̀
 - ``sudo nano pricebot.py``̀
 - ``py pricebot.py``̀
 - Remove the comment ``̀#``̀ from the ``̀api.update_status(status=twittertemplate)``̀  Line at the end to "go live" and actually tweet out
 
 **Variables** <br>
``CryptoSlugstoretrieve`` List of all Coinnames to retrieve, Example => 'bitcoin,ethereum,mimblewimblecoin,compound' <br>
``convertto`` Name of Coin to convert to (show price in) Example => 'USD' <br>
``extractedpricedata = []`` Dont touch - needed to run <br>
``tmp = ''`` Dont touch - needed to run <br>
``slugorname`` Set's Displaystyle of Coins, either their 'symbol'  'slug' or 'name'<br>
``seperatorstring`` Is what's between the Coins Name and it's price in the template, by Default ' = '<br>
``timebetweentweets`` Time between Tweets, by default 14400 in seconds  <br>

**Credits** <br>
to ryanc20(https://github.com/ryanc20/crypto-twitter-bot/blob/master/crypto_bot_no_key.py) as I saw how easy such a small wrapper should be, although in the end no Code is copied (as they are the official tweepy API doc examples) 
