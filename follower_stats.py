import tweepy as tw


auth = tw.OAuthHandler('consumer_key','consumer_secret') #insert consumer_key and consumer_secret
auth.set_access_token('access_token','access_token_secret') #insert access_token and access_token_secret

api = tw.API(auth, wait_on_rate_limit=True)

username = input("Enter a Twitter Username: ")
user=api.get_user(username)
num_of_followers=user.followers_count
num_of_friends=user.friends_count
print(str(username)+ " has " +str(num_of_followers) +" followers")
print(str(username)+ " is following " +str(num_of_friends) +" people")
following_follower_ratio=round(num_of_followers/num_of_friends,2)
print(str(username)+ "'s following/follower ratio is " +str(following_follower_ratio) +" people")


