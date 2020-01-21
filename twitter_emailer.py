import tweepy as tw 
import smtplib
from email.message import EmailMessage
from datetime import datetime,date,timedelta

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)

username = input("Enter a Twitter Username you'd like to get tweets in email for: ")

def collect_tweets(username):
    count=0
    yesterdays_tweets = []
    try:
        tmpTweets = api.user_timeline(username)
    except:
        print("Please check the username you entered")
         
    for t in tmpTweets:
        if t.created_at.date()+timedelta(hours=5.5) == datetime.now().date()+timedelta(days=-1):
            if t.in_reply_to_status_id is None:
                #print(t.text)
                count+=1
                yesterdays_tweets.append(t.text)

    #print(str(count) + " tweets yesterday")
    
    return yesterdays_tweets


def email_tweets(username,yesterdays_tweets):

    sender_email = "a@gmail.com"  # Enter your address
    receiver_email = "d@gmail.com"  # Enter receiver address

    #Subject: Yesterday's Tweets Summary: """ + str(username) + """ """ +str(len(yesterdays_tweets)) + """
    message = f"""\
    Subject: Yesterday's Tweets Summary
    To: {receiver_email}
    From: {sender_email}
    

    """
    for tw in yesterdays_tweets:
        tw = tw.encode('ascii', 'ignore').decode('ascii')
        message = message + """Tweet # """ + str(tw) + " \n"

    print(message)
    

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("email id", "password") #email id and password
    server.sendmail(sender_email,receiver_email,message)



yesterdays_tweets = collect_tweets(username)
email_tweets(username,yesterdays_tweets)