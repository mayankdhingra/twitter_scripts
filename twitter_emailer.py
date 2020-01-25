import tweepy as tw 
import smtplib
from email.message import EmailMessage
from datetime import datetime,date,timedelta

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)

username = input("Enter a Twitter Username you'd like to get tweets in email for: ")
users = username.split(',')

#def get_tweet_text(tweet):
#    print(tweet.truncated)
#    if tweet.truncated:
#        text = tweet.full_text
#    else:
#        text = tweet.text
#    return text

def collect_tweets(users):
    yesterdays_tweets = []
    for username in users:
        #print(username,"username")
        count=0
        startDate=endDate=datetime.now().date()+timedelta(days=-1)
    
        try:
            tmpTweets = api.user_timeline(username)
            #results = [status._json for status in tw.Cursor(API.search, q=username, count=1000, tweet_mode='extended', lang='en').items()]
            #print(len(results),"aaaaaa")
        except:
            print("Please check the username you entered")
        
        for t in tmpTweets:
            #print(t.created_at," ",datetime.now().date()+timedelta(days=-1))
            
            if t.created_at.date()+timedelta(hours=5.5) == datetime.now().date()+timedelta(days=-1):
                if t.in_reply_to_screen_name==username or t.in_reply_to_status_id is None:
                    #print(t.created_at)
                    count+=1
                    yesterdays_tweets.append(t.text)
        #print(tmpTweets[-1].created_at.date()+timedelta(hours=5.5) == startDate,"here",startDate)        
        #print(type(tmpTweets[-1].created_at.date()+timedelta(hours=5.5)), type(startDate),"here",startDate)        
        while (tmpTweets[-1].created_at.date()+timedelta(hours=5.5) == startDate):
            #print(tmpTweets[-1].created_at,"here")
            tmpTweets = api.user_timeline(username,max_id=tmpTweets[-1].id)
            for tweet in tmpTweets:
                if tweet.created_at.date()+timedelta(hours=5.5) == endDate and tweet.created_at.date()+timedelta(hours=5.5) == startDate and tweet not in yesterdays_tweets:
                    yesterdays_tweets.append(tweet.text)
                        
    # for debugging missing tweets
    #            else:
    #                print(t.text, t.in_reply_to_screen_name, t.created_at)


        #print(str(count) + " tweets yesterday")
        #print("total tweets",len(yesterdays_tweets))
    return yesterdays_tweets


def email_tweets(username,yesterdays_tweets):
    if yesterdays_tweets:
        sender_email = "a@gmail.com"  # Enter your address
        receiver_email = "d@gmail.com"  # Enter receiver address
        tweet_number=1

        #Subject: Yesterday's Tweets Summary: """ + str(username) + """ """ +str(len(yesterdays_tweets)) + """
        
        SUBJECT = "Yesterday's Tweets Summary For: " + username
        TEXT = "\n"
        
        for tw in yesterdays_tweets:
            tw = tw.encode('ascii', 'ignore').decode('ascii')
            TEXT = TEXT + """Tweet """ +str(tweet_number) + ": "+ str(tw) + " \n"
            tweet_number+=1

        print(TEXT)

        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("email id", "password") #email id and password
        server.sendmail(sender_email,receiver_email,message)
        print("Email Sent")
        server.quit()

yesterdays_tweets = collect_tweets(users)
email_tweets(username,yesterdays_tweets)