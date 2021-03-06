import tweepy as tw 
import datetime,requests,re


auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)

def url_expander(url):
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    expanded_url=resp.url
    return expanded_url 

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
tweets_longlist,tweets_shortlist = [],[]
tweets_shortlist.append(thread_start_status)
#print(tweets_shortlist)
try:
	tmpTweets = api.user_timeline(username,tweet_mode='extended',include_entities=True)
except:
	print("Please check the username you entered")		

for tweet in tmpTweets:
    if tweet.created_at < thread_end_date and tweet.created_at >= thread_start_date:
        #print(tweet.full_text)
        tweets_longlist.append(tweet)
#print("\n",thread_start_date,thread_end_date,tmpTweets[-1].created_at,len(tweets_longlist))
while (tmpTweets[-1].created_at > thread_start_date):
    tmpTweets = api.user_timeline(username,max_id=tmpTweets[-1].id,tweet_mode='extended')
    for tweet in tmpTweets:
        if tweet.created_at < thread_end_date and tweet.created_at > thread_start_date and tweet not in tweets_longlist:
            tweets_longlist.append(tweet)
tweets_longlist = tweets_longlist[::-1]

previous_tweet_id=int(thread_start_id)

for tweet in tweets_longlist:
    #print(tweet._json['id'],tweet._json['in_reply_to_status_id'],previous_tweet_id)
    #print("here",tweet._json['in_reply_to_status_id'],previous_tweet_id,tweet._json['in_reply_to_status_id']==previous_tweet_id)
    if tweet._json['in_reply_to_status_id']==previous_tweet_id:
        #print("here1")
        tweets_shortlist.append(tweet)
        previous_tweet_id=tweet._json['id']


print(f"Tweetstorm by @{username} comprising of {len(tweets_shortlist)} tweets, URL: {thread_url}\n")
print("-------------------------------------------------------------------------------------------------------------------------------------")
for tweet in tweets_shortlist:
    text = tweet.full_text
    #print(old_text)
    old_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    if old_url:
        old_url=old_url[0]
        new_url = url_expander(old_url) 
        text =  tweet.full_text.replace(old_url,new_url)
    print(text)
    if 'media' in tweet.entities: #print urls for images from the tweets
        for media in tweet.extended_entities['media']:
            print(media['media_url'])
    print("\n")
print("-------------------------------------------------------------------------------------------------------------------------------------")
