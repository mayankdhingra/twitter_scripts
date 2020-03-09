import tweepy as tw
import datetime,statistics
from datetime import timedelta,datetime

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)

username = input("Enter a Twitter Username: ")

def convert_date_duration(startdate,enddate):
	day, month, year = map(int,start_date_entry.split('-'))
	startDate = datetime(year,month,day,0,0,0)
	day, month, year = map(int,end_date_entry.split('-'))
	endDate = datetime(year,month,day,23,59,59)
	
	return {'startDate':startDate,'endDate':endDate}

def do_user_analysis(username):
    user=api.get_user(username)
    num_of_followers=user.followers_count
    num_of_friends=user.friends_count
    lists=user._json['listed_count']
    following_follower_ratio=round(num_of_followers/num_of_friends,2)
    bio=user.description
    joining_date=datetime.strptime(user._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    tweets_count=user._json['statuses_count']
    return {'lists':lists   ,'followers':num_of_followers,'following':num_of_friends,'following_follower_ratio':following_follower_ratio,'joining_date':joining_date,'tweets_count':tweets_count,'bio':bio}

def do_tweets_analysis(username,startDate,endDate):
	duration = ((endDate-startDate).days)+1
	if duration<=0:
		print("Please check start and end dates you entered")
	else:	
		total_retweet_count=0
		tweets_with_noengagement=0
		total_likes_count=0
		tweets=[]
		hours=[]
		tweet_length=[]
		orignal_tweets=0
		new_tweets=0
		rt_of_others=0
		reply_to_others=0

		try:
			tmpTweets = api.user_timeline(username)
		except:
			print("Please check the username you entered")
		for tweet in tmpTweets:
			if tweet.created_at+timedelta(hours=5.5) < endDate and tweet.created_at+timedelta(hours=5.5) > startDate:
				tweets.append(tweet)
				hours.append((tweet.created_at+timedelta(hours=5.5)).hour)
				tweet_length.append(len(tweet.text))			
		#while (tmpTweets[-1].created_at+timedelta(hours=5.5) > startDate):
		while (tmpTweets[-1].created_at > startDate):
			tmpTweets = api.user_timeline(username,max_id=tmpTweets[-1].id)
			for tweet in tmpTweets:
				#print(tweet.text,tweet.created_at,endDate,startDate)
				if tweet.created_at+timedelta(hours=5.5) < endDate and tweet.created_at+timedelta(hours=5.5) > startDate and tweet not in tweets:
				#if tweet.created_at < endDate and tweet.created_at > startDate and tweet not in tweets:
					tweets.append(tweet)
					hours.append((tweet.created_at+timedelta(hours=5.5)).hour)
					tweet_length.append(len(tweet.text))
					#print(tweets)
		for t in tweets:
			if t.in_reply_to_status_id is not None:
				reply_to_others+=1
			elif hasattr(t, 'retweeted_status') or t.is_quote_status==True:
				rt_of_others+=1
			else:
				if t.retweet_count==0:
					if t.favorite_count==0:
						tweets_with_noengagement+=1
					else:
						total_likes_count+=t.favorite_count
				else:
					total_retweet_count+=t.retweet_count
					if t.favorite_count>0:
						total_likes_count+=t.favorite_count
		orignal_tweets=len(tweets)-rt_of_others
		new_tweets=	len(tweets)-rt_of_others-reply_to_others
		return {'tweets':tweets,'hours':hours,'tweet_length':tweet_length,'rt_of_others':rt_of_others,'reply_to_others':reply_to_others,'orignal_tweets':orignal_tweets,'new_tweets':new_tweets,'total_likes_count':total_likes_count,'total_retweet_count':total_retweet_count,'tweets_with_noengagement':tweets_with_noengagement,'duration':duration}

try:
	start_date_entry = input('Enter a start date in DD-MM-YYYY format: ')
	end_date_entry   = input('Enter an end date in DD-MM-YYYY format: ')
	dates = convert_date_duration(start_date_entry,end_date_entry)
	startDate=dates['startDate']
	endDate=dates['endDate']
	
except:
	print("Please check start and end dates")

dict = do_tweets_analysis(username,startDate,endDate)
#too lazy to change variables used in print functions
tweets = dict['tweets']
hours = dict['hours']
tweet_length = dict['tweet_length']
rt_of_others = dict['rt_of_others']
reply_to_others = dict['reply_to_others']
orignal_tweets = dict['orignal_tweets']
new_tweets = dict['new_tweets']
total_likes_count = dict['total_likes_count']
total_retweet_count = dict['total_retweet_count']
tweets_with_noengagement = dict['tweets_with_noengagement']
duration= dict['duration']
dict_user=do_user_analysis(username)
lists=dict_user['lists']
followers=dict_user['followers']
following=dict_user['following']
following_follower_ratio=dict_user['following_follower_ratio']
joining_date=dict_user['joining_date']
tweets_count=dict_user['tweets_count']
bio=dict_user['bio']
print("User Analysis (@"+str(username) +") \n-----------")
print(f"Using Twitter Since: {str(joining_date.date())}")
print(f"Bio: {str(bio)}")
print(f"Tweet Count: {str(tweets_count)}")
print(f"Followers Count: {str(followers)}")
print(f"Following Follower Ratio: {str(following_follower_ratio)}")
print(f"List Part Of: {str(lists)}")
print("\n")
print("Tweet Analysis \n-----------")
print(username+ " has Tweeted " + str(len(tweets)) + " times over " + str(duration) + " days")
if len(tweets)>0:
	print(f"Average Tweets Per Day: {round((len(tweets)/duration),2)}")
	print(username+"'s Peak Hour for Tweeting is between "+str(max(hours,key=hours.count)) + " and " + str(max(hours,key=hours.count)+1) +" Hours")
	print(username+"'s Average Tweet is " +str(round(statistics.mean(tweet_length)))+" characters long")
	#print(username+"'s Lean Hour for Tweeting is between "+str(min(hours,key=hours.count)) + " and " + str(min(hours,key=hours.count)+1) +" Hours")
	print(f"New Tweets:  {len(tweets)-rt_of_others-reply_to_others}, Replies to Others: {reply_to_others}, Retweets of Others: {rt_of_others}")
	print(username+"'s original tweet ratio (new tweets + replies to others): " + str(round(orignal_tweets*100/len(tweets),2)) + "%")
	print(username+"'s new tweet ratio (excl replies to others and RTs): " + str(round(new_tweets*100/len(tweets),2)) + "%")
	print(f"{len(tweets)-rt_of_others-reply_to_others} New Tweets got {total_likes_count} Likes and {total_retweet_count} Retweets")
	if new_tweets>0:
		print(f"% Tweets with Engagement: {round((new_tweets-tweets_with_noengagement)*100/new_tweets,2)} %" )
	print(f"Average Engagement Per Tweet: {round(total_likes_count/len(tweets),2)} Likes Per Tweet, {round(total_retweet_count/len(tweets),2)} Retweets Per Tweet")
	print("-----------")




		
