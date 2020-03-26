import tweepy as tw
import datetime,statistics
from datetime import timedelta

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret


api = tw.API(auth, wait_on_rate_limit=True)
username = input("Enter a Twitter Username: ")
word = input("Enter a Word (not phrase) that you want to find first mention: ")

def get_status_url(username,status_id):    
        status=api.get_status(status_id, include_entities=True)    
        status_url="https://twitter.com/"+str(username)+"/status/"+str(status_id)
        return status_url

def get_status_text(status_id): 
    status=api.get_status(status_id, tweet_mode='extended')
    if hasattr(status,'retweeted_status'):
        text = "RT @" + str(status._json['retweeted_status']['user']['screen_name']) + ": " + str(status._json['retweeted_status']['full_text'])
    else:
        if hasattr(status,'extended_status'):
            text = status.extended_tweet['full_text']
        else:
            text = status.full_text
    return text

def convert_date_duration(startdate,enddate):
	day, month, year = map(int,start_date_entry.split('-'))
	startDate = datetime.datetime(year,month,day,0,0,0)
	day, month, year = map(int,end_date_entry.split('-'))
	endDate = datetime.datetime(year,month,day,23,59,59)
	
	return {'startDate':startDate,'endDate':endDate}
 	
def do_tweets_analysis(username,startDate,endDate):
    duration = ((endDate-startDate).days)+1
    if duration<=0:
        print("Please check start and end dates you entered")
    else:
        no_of_mentions=0
        mention_tweets,mention_dates,tweets=[],[],[]
        try:
            tmpTweets = api.user_timeline(username,tweet_mode='extended',include_entities=True)
        except:
            print("Please check the username you entered")

        for tweet in tmpTweets:
            if tweet.created_at+timedelta(hours=5.5) < endDate and tweet.created_at+timedelta(hours=5.5) > startDate:
                tweets.append(tweet)
                if tweet.full_text.find(word) >= 0:
                    mention_tweets.append(tweet.id)
                    mention_dates.append(tweet.created_at.date())
        while (tmpTweets[-1].created_at > startDate):
            tmpTweets = api.user_timeline(username,max_id=tmpTweets[-1].id,tweet_mode='extended',include_entities=True)
            for tweet in tmpTweets:
                if tweet.created_at+timedelta(hours=5.5) < endDate and tweet.created_at+timedelta(hours=5.5) > startDate and tweet not in tweets:
                    tweets.append(tweet)
                    if tweet.full_text.find(word)>=0:
                        mention_tweets.append(tweet.id)
                        mention_dates.append(tweet.created_at.date())
        no_of_mentions = len(mention_tweets)
        return {'no_of_mentions':no_of_mentions,'mention_dates':mention_dates,'mention_tweets':mention_tweets}

try:
	start_date_entry = input('Enter a start date in DD-MM-YYYY format: ')
	end_date_entry   = input('Enter an end date in DD-MM-YYYY format: ')
	dates = convert_date_duration(start_date_entry,end_date_entry)
	startDate=dates['startDate']
	endDate=dates['endDate']
	
except:
	print("Please check start and end dates")

dict = do_tweets_analysis(username,startDate,endDate)
mention_dates = dict['mention_dates']
mention_tweets = dict['mention_tweets']	
no_of_mentions = dict['no_of_mentions']	
print(username+ " first Tweeted about " +str(word) + " on " + str(mention_dates[-1].day) + "-" + str(mention_dates[-1].month) + "-" + str(mention_dates[-1].year) + " and has tweeted about " + str(word) + " on" + str(no_of_mentions) + " times")
print(username + " 's first tweet was ------- \n" +str(get_status_text(mention_tweets[-1])) + "------- \n") 
print(get_status_url(username,mention_tweets[-1]))




		
