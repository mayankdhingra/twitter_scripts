import tweepy as tw
import sys,datetime
#from datetime import datetime

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret


api = tw.API(auth, wait_on_rate_limit=True)
#username = sys.argv[1]
username = input("Enter Your Twitter Username: ")
tweets=[]
start_date_entry = input('Enter a start date in DD-MM-YYYY format: ')
end_date_entry   = input('Enter an end date in DD-MM-YYYY format: ')
day, month, year = map(int, start_date_entry.split('-'))
startDate = datetime.datetime(year, month, day,0 ,0, 0)
#d1 = datetime.strptime(startDate, "%Y-%m-%d")
#print(startDate)
day, month, year = map(int, end_date_entry.split('-'))
endDate = datetime.datetime(year, month, day, 0, 0, 0)
duration=((endDate-startDate).days)


#d2 = datetime.strptime(endDate, "%Y-%m-%d")
#num_of_days = abs((d2-d1).days)
#print(num_of_days)
#print(endDate)

# startDate = datetime.datetime(2019, 12, 1, 0, 0, 0)
if duration<=0:
	print("Please check start and end dates you entered")
else:	
	retweet_count=0
	try:
		tmpTweets = api.user_timeline(username)
		for tweet in tmpTweets:
		    if tweet.created_at < endDate and tweet.created_at > startDate:
		        tweets.append(tweet)
		        #print(tweet.text,len(tweets))

		while (tmpTweets[-1].created_at > startDate):
			tmpTweets = api.user_timeline(username, max_id=tmpTweets[-1].id)
			for tweet in tmpTweets:
				if tweet.created_at < endDate and tweet.created_at > startDate and tweet.id not in tweets:
					tweets.append(tweet)
					#print(tweet.text,len(tweets))

		for tw in tweets:
			if hasattr(tw, 'retweeted_status'):	
				retweet_count+=1

		print(username + " has made " + str(len(tweets)) + " tweets between " + str(start_date_entry) + " and " + str(end_date_entry) + " out of which " + str(retweet_count) + " are retweets")
		print(username	+"'s original tweet ratio is " + str(round((len(tweets)-retweet_count)/len(tweets)*100,2)) + "%") 
	except:
		print("Please check the username you entered")