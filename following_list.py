import tweepy as tw 
from datetime import timedelta,datetime

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)

foll_list = []
following_last_tweet = {}


def following_names():
    threshold = datetime(2020,7,1,0,0,0) #date after which if someone hasn't tweeted they can be called inactive
    inactive_count=1
    #count=1
    for user in tw.Cursor(api.friends, screen_name='userwhosefollowersyouwanttosee').items():
        last_tweet_date=user_last_tweet_date(user.screen_name)
        if last_tweet_date!='No Tweets' and last_tweet_date < threshold:
            last_tweet_date=last_tweet_date.strftime("%d/%m/%Y")
            print('inactive user: ' + str(inactive_count) + ' ' + user.screen_name + '-->' + last_tweet_date)
            inactive_count=inactive_count+1
        #print(count)
        #count=count+1
    return foll_list



def user_last_tweet_date(username):
    tmpTweets = api.user_timeline(username)
    if tmpTweets:
        last_tweet_date=tmpTweets[0].created_at+timedelta(hours=5.5)
        return last_tweet_date
    else:
        return 'No Tweets'
    


foll_list = following_names()
