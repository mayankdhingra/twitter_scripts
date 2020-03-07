import tweepy as tw
import datetime, random, smtplib
from datetime import timedelta

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret
api = tw.API(auth, wait_on_rate_limit=True)

user = 'naval' #insert the username for whose random favorite tweet you'd like to get over email
all_fav_tweets = []
old_date = datetime.datetime(2019,1,1,0,0,0)
tweets=api.favorites(user,tweet_mode='extended',include_entities=True)

sender_email = "a@gmail.com"  # Enter your address
receiver_email = "d@gmail.com"  # Enter receiver address

for t in tweets:
    all_fav_tweets.append(t._json['id'])
print(f"Fetched {len(all_fav_tweets)} tweets, fetching more")

while (tweets[-1].created_at>old_date and len(all_fav_tweets)<=1000):
    tweets=api.favorites(user,max_id=tweets[-1].id,tweet_mode='extended',include_entities=True)
    for t in tweets:
    
        all_fav_tweets.append(t._json['id'])
    print(f"Fetched {len(all_fav_tweets)} tweets, fetching more")
random_tweet_id=all_fav_tweets[random.randint(0,len(all_fav_tweets))]
random_tweet=api.get_status(random_tweet_id,tweet_mode='extended',include_entities=True)
random_tweet_text=random_tweet._json['full_text']
random_tweet_user=random_tweet._json['user']['screen_name']
random_tweet_url = "https://twitter.com/"+str(random_tweet_user)+"/status/"+str(random_tweet_id)


SUBJECT = "Random Liked Tweet For The Day"
TEXT = "\nTweet By "
TEXT = TEXT + str(random_tweet_user) + ": " +str(random_tweet_text) + "\n\n" + str(random_tweet_url)
message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
print(message)
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("email id", "password") #email id and password

message= message.encode('ascii', 'ignore').decode('ascii')
server.sendmail(sender_email,receiver_email,message)
print("Email Sent")
server.quit()



