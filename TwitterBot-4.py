#!/usr/bin/env python
# coding: utf-8

# In[79]:


#Austin Cox and Nick Kalinowski
#The bot uses twitter handle @cryptobot190
#To test, tweet either btc or bitcoin to get the current bitcoin price
#or tweet info or help for a support tweet
#!/usr/bin/env python
# coding: utf-8

# In[75]:


import tweepy
import logging
import time
import json
import requests
import pandas

#Creating api to connect to twitter
def create_api():
    consumer_key = 'xAPWhU0vSaf4ukceuzIvN0y2C'
    consumer_secret = 'A1rppsl9UKGGuN3MSWrNVftTLo8eUQB95jXw8bHZl4dHVAIN5S'
    access_token = '1470210043001847817-yYBN0edlHxv9Ul7odtar1fQq9zfgJV'
    access_token_secret = 'ORedkbYCR8w1jbGnqBvauBbyiTJeSxWjcrv1QYlNVR0R9'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logging.error("Error creating API", exc_info=True)
        raise e
    logging.info("API created")
    
    return api

since_id = 1

api = create_api()
tweets = list(tweepy.Cursor(api.mentions_timeline, since_id=since_id).items())

seen = set()

#This portion checks mentions for bitcoin or btc, converts the tweet to all lowercase, and then pulls from the yahoo
#finance API the current price of bitcoin and returns the current price and date to the user as a reply to the last
#tweet
def check_mentions(api, keywords, since_id):
    logging.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        try:
            if tweet.id in seen:
                continue
            if any(keyword in tweet.text.lower() for keyword in keywords):
                seen.add(tweet.id)
                logging.info(f"Answering to {tweet.user.name}")
                yfapikey='jIEHPVdf8227Vj0QfSs7H5wIrowhRVWi9wvTGjVp'
                url = "https://yfapi.net/v6/finance/quote"
                quote = "BTC-USD"
                querystring = {"symbols": quote}
                headers = {
                     'x-api-key': yfapikey
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                btc_json = response.json()
                mkt_time = btc_json['quoteResponse']['result'][0]["regularMarketTime"]
                mkt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(mkt_time))
                price = btc_json['quoteResponse']['result'][0]["regularMarketPrice"]
                reply = " As of"+" "+mkt_time+" "+"the current price of Bitcoin is $"+str(price)
                print(reply)

                api.update_status(
                    status=f'@{tweet.author.screen_name}'+str(reply),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
        except Exception as e:
            logging.error("Error executing", exc_info=True)
            raise e
    return new_since_id

#The help commands functions in the same way, only it looks for keywords help or info, rather than bitcoin related ones
def help_commands(api, new_keywords, since_id):
    logging.info("Retrieving mentions")
    new_help_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_help_id = max(tweet.id, new_help_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        try:
            if tweet.id in seen:
                continue
            if any(keyword in tweet.text.lower() for keyword in new_keywords):
                seen.add(tweet.id)
                help_message = "Mention this bot with 'btc' or 'bitcoin' to get the current price"
                print(help_message)
        
                api.update_status(
                    status=f'@{tweet.author.screen_name}'+str(help_message),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True)
        except Exception as e:
            logging.error("Error executing", exc_info=True)
            raise e
    return new_help_id

#The main function pulls everything together and runs the corresponding code if/when the correct keywords are mentioned
def main():
    api = create_api()
    since_id = 1
    help_id = 1
    while True:
        since_id = check_mentions(api, ["btc", "bitcoin"], since_id)
        help_id = help_commands(api, ["help", "info"], help_id)
        logging.info("Waiting...")
        time.sleep(10)
if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




