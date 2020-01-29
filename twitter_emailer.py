import tweepy as tw 
import smtplib
from email.message import EmailMessage
from datetime import datetime,date,timedelta

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret


api = tw.API(auth, wait_on_rate_limit=True)

username = input("Enter a Twitter Username you'd like to get tweets in email for: ")
users = username.split(',')


def collect_tweets(users):
    yesterdays_tweets = []

    def get_status_text(status):

        if hasattr(status,'retweeted_status'):
            text = status._json['retweeted_status']['full_text']
        else:
            if hasattr(status,'extended_status'):
                text = status.extended_tweet['full_text']
            else:
                text = status.full_text
        return text

    for username in users:
        #print(username,"username")
        count=0
        startDate=endDate=datetime.now().date()+timedelta(days=-1)
    
        try:
            tmpTweets = api.user_timeline(username)
            for status in tw.Cursor(api.user_timeline, id=username, tweet_mode='extended').items():
                if status.created_at.date()+timedelta(hours=5.5) == datetime.now().date()+timedelta(days=-1):
                    if status.in_reply_to_screen_name==username or status.in_reply_to_status_id is None:
                        count+=1
                        yesterdays_tweets.append(get_status_text(status))
            #print(len(results),"aaaaaa")
        except:
            print("Please check the username you entered")
    return yesterdays_tweets


def email_tweets(username,yesterdays_tweets):
    if yesterdays_tweets:
        sender_email = "a@gmail.com"  # Enter your address
        receiver_email = "d@gmail.com"  # Enter receiver address
        tweet_number=1

        #Subject: Yesterday's Tweets Summary: """ + str(username) + """ """ +str(len(yesterdays_tweets)) + """
        
        SUBJECT = "Yesterday's Tweets Summary For:" + username
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