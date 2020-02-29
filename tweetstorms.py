import tweepy as tw 
import datetime


auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)


thread_url=input("Please enter the tweetstorm you want to download: ")
thread_start_id=thread_url.split('/status/')[1]
thread_start_status=api.get_status(thread_start_id,tweet_mode='extended')
thread_start_date=thread_start_status.created_at
if thread_start_date.day>26: #assumption - almost all people will tweet a tweestorm over three days           
    thread_end_date = datetime.datetime(thread_start_date.year,thread_start_date.month+1,1,23,59,59) 
else:   
    thread_end_date = datetime.datetime(thread_start_date.year,thread_start_date.month,thread_start_date.day+1,23,59,59) #assumption - almost all people will tweet a tweestorm over three days

#thread_end_date = datetime.datetime(thread_start_date.year,thread_start_date.month,thread_start_date.day+2,23,59,59) #assumption - almost all people will tweet a tweestorm over three days
username=thread_url.split('/status/')[0].split('/')[3]
#status=api.get_status(thread_start_id, tweet_mode='extended')
#print("user",username,"id",thread_start_id,"start date",thread_start_status.created_at,"end date",thread_end_date)
#print(thread_start_status.created_at.date())
tweets_longlist,tweets_shortlist = [],[]
tweets_shortlist.append(thread_start_status)

try:
	tmpTweets = api.user_timeline(username,tweet_mode='extended')
except:
	print("Please check the username you entered")		

for tweet in tmpTweets:
    if tweet.created_at < thread_end_date and tweet.created_at > thread_start_date:
        tweets_longlist.append(tweet)

while (tmpTweets[-1].created_at > thread_start_date):
    tmpTweets = api.user_timeline(username,max_id=tmpTweets[-1].id,tweet_mode='extended')
    for tweet in tmpTweets:
        if tweet.created_at < thread_end_date and tweet.created_at > thread_start_date and tweet not in tweets_longlist:
            tweets_longlist.append(tweet)
tweets_longlist = tweets_longlist[::-1]

previous_tweet_id=int(thread_start_id)

for tweet in tweets_longlist:
    #print("here",tweet._json['in_reply_to_status_id'],previous_tweet_id,tweet._json['in_reply_to_status_id']==previous_tweet_id)
    if tweet._json['in_reply_to_status_id']==previous_tweet_id:
        #print("here1")
        tweets_shortlist.append(tweet)
        previous_tweet_id=tweet._json['id']

print(f"Tweetstorm by @{username} comprising of {len(tweets_shortlist)} tweets\n")
print("-------------------------------------------------------------------------------------------------------------------------------------")
for tweet in tweets_shortlist:    
    print(tweet.full_text,"\n")
print("-------------------------------------------------------------------------------------------------------------------------------------")