import tweepy as tw
from datetime import date
import sys

auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret
stats_file = r"/Users/twitter_scripts/daily_twitter_stats"  # name of my log file

#secrets = json.loads(open(path + 'secrets.json').read())
api = tw.API(auth, wait_on_rate_limit=True)


# Function to save daily follower and following counts in a JSON file
def todays_stats():
  # Get my account information
  info = api.me()
  # Get follower and following counts
  followers_cnt = info.followers_count  
  following_cnt = info.friends_count
  # Get today's date
  today = date.today()
  d = today.strftime("%b %d, %Y")
  stats = "Date: " + str(d) + "; followers: " + str(followers_cnt) +"; following: " +str(following_cnt)  
  return stats

def write_stats(text,file):
    f = open(file, 'a+')           # 'a' will append to an existing file if it exists and create it if it doesn't
    f.write("{}\n".format(text))  # write the text to the stats file and move to next line
    return 


write_stats(todays_stats(),stats_file)

