import tweepy as tw 
import smtplib
from email.message import EmailMessage
from datetime import datetime,date,timedelta
from collections import OrderedDict

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)

user_name = input("Enter Twitter Usernames (seperated by comma) you'd like to get tweets in email for: ")
users = user_name.split(',')



def collect_tweets(users):
    yesterdays_tweets = []
    yesterdays_tweets_details={} # {u1:{id1:[type1,text1,link1],id2:[type2,text2,link2]},u2:{id1:[type1,text1,link1],id2:[type2,text2,link2]}}
    
    def get_status_text(status_id): 
        # s.entities['media'][0]['media_url'] media url
        status=api.get_status(status_id, tweet_mode='extended')
        if hasattr(status,'retweeted_status'):
            text = "RT @" + str(status._json['retweeted_status']['user']['screen_name']) + ": " + str(status._json['retweeted_status']['full_text'])            
        else:
            if hasattr(status,'extended_status'):
                text = status.extended_tweet['full_text']
            else:
                text = status.full_text
        
        return text

    def get_status_url(status_id):
        print(status_id)
        status=api.get_status(status_id, include_entities=True)
        print(status.entities['urls'][0]['expanded_url'])
        status_url=status.entities['urls'][0]['expanded_url']  
        return status_url

    for username in users:
        
        users_yday_tweets = OrderedDict() 
        #users_yday_tweets={}
        count=0
        startDate=endDate=datetime.now().date()+timedelta(days=-1)
        
        try:
            
            for status in tw.Cursor(api.user_timeline, id=username, tweet_mode='extended',include_entities=True).items():
                
                if status.created_at.date()+timedelta(hours=5.5) == datetime.now().date()+timedelta(days=-1):
                    if status.in_reply_to_screen_name==username or status.in_reply_to_status_id is None:
                        count+=1
                        #print(status.id)
                        #print(get_status_text(status.id))
                        #print(status.entities['urls'])
                        #if status.entities['urls']:
                        #    print(get_status_url(status.id))
                        #users_yday_tweets[status.id]=[get_status_text(status.id),get_status_url(status.id)]
                        users_yday_tweets[status.id]=[get_status_text(status.id)]
                        #else:
                        #    users_yday_tweets[status.id]=[get_status_text(status.id),'']

            users_yday_tweets_reversed = OrderedDict()
            for k in reversed(users_yday_tweets):
                users_yday_tweets_reversed[k] = users_yday_tweets[k]
            yesterdays_tweets_details[username]=users_yday_tweets_reversed
            #yesterdays_tweets_details[username]=dict(sorted(users_yday_tweets.items(), key=operator.itemgetter(1)))

        except:
            print("Please check the username you entered")
    
    return yesterdays_tweets_details


def email_tweets(users,yesterdays_tweets):
    #yesterdays_tweets_text=[]
    
    #yesterdays_tweets_text=yesterdays_tweets[username]
    

    #for tw in yesterdays_tweets:   
        #yesterdays_tweets_details[tw]=get_status_text(tw)
        #yesterdays_tweets_text.append(get_status_text(t))

    if yesterdays_tweets:

        sender_email = "a@gmail.com"  # Enter your address
        receiver_email = "d@gmail.com"  # Enter receiver address
        tweet_number=1

        #Subject: Yesterday's Tweets Summary: """ + str(username) + """ """ +str(len(yesterdays_tweets)) + """
        
        SUBJECT = "Yesterday's Tweets Summary For: " + "{} and {}".format(", ".join(users[:-1]),  users[-1])
        TEXT = "\n"
        
        for user in users:
            tweets=yesterdays_tweets[user]
            if tweets:
                TEXT = TEXT + "Tweets By " + user + "\n\n"
                for tw in tweets:
                    txt = tweets[tw][0]
                    TEXT = TEXT + """Tweet """ +str(tweet_number) + ": "+ str(txt) +  " \n"
                    tweet_number+=1
                TEXT= TEXT + "\n\n"
            else:
                TEXT = TEXT + "No Tweets By " + user + "yesterday"
        

        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        print(message)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("email id", "password") #email id and password
        message= message.encode('ascii', 'ignore').decode('ascii')
        server.sendmail(sender_email,receiver_email,message)
        print("Email Sent")
        server.quit()

yesterdays_tweets = collect_tweets(users)
email_tweets(users,yesterdays_tweets)