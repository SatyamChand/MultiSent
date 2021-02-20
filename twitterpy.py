import json
import tweepy
import sentimentpy


last_status_id = 0


class Twitter:

	def __init__(self):
		with open('twitter_login_data.json','r') as auth_file:
			auth_json = json.load(auth_file)
		# consumer_key = 'JrpXfhcf4gW5G8VZnWxRM759c'
		# consumer_password = 'xo6xOOHizjehxDQjtb5xXsn6T7hRHTSHApHVkXDQBpjty0XGdO'
		
		# access_token = '1218437860233101312-B5vukgKw7scPMBxr5OyoSkTnMIHAyS'
		# access_token_secret = 'jdk8LPApXANbU5jEHIfmWy81rIwNUeZMeIX1r4SOwWt4D'

		auth = tweepy.OAuthHandler(auth_json['consumer_key'],auth_json['consumer_password'])
		auth.set_access_token(auth_json['access_token'],auth_json['access_token_secret'])

		self.api = tweepy.API(auth)


	def home_user():
		username = self.api.me()
		print(username)
		return username


	def get_timeline(self, username='' ):
		if username == '':
			self.api.me()
		user = self.api.get_user(username)
		timeline = user.timeline(tweet_mode='extended')
		return timeline


	def get_tweets_for_page(self, username='' ):
		if username == '':
			self.api.me()
		user = self.api.get_user(username)
		timeline = user.timeline(tweet_mode='extended')
		output=[]
		sen_list=[]
		#print(dir(timeline[0]))
		for tweet in timeline:
			screen_name = tweet.user.screen_name
			text = tweet.full_text
			sentiment = sentimentpy.find_sentiment(text)
			sen_list.append(sentiment)
			output.append( { 'screen_name': screen_name, 'text': text, 'sentiment': sentiment } )
		return output,sen_list


	def get_mentions_with_cursor(self, username):
		global last_status_id
		output=[]
		sen_list=[]
		top_status_id = 1
		csr = tweepy.Cursor(self.api.search, q=username, tweet_mode="extended")
		top = True

		for tweet in csr.items(20):
			if top:
				top_status_id = tweet.id
				top = False
			
			if tweet.id == last_status_id:
				break;

			screen_name = tweet.user.screen_name
			text = tweet.full_text
			sentiment = sentimentpy.find_sentiment(text)
			sen_list.append(sentiment)
			output.append( { 'screen_name': screen_name, 'text': text, 'sentiment': sentiment } )
			#print(tweet.full_text)

		last_status_id = top_status_id
		return output,sen_list


	def get_timeline_with_cursor(self, username):
		global last_status_id
		output = []
		sen_list = []
		top_status_id = 1
		csr = tweepy.Cursor(self.api.timeline, q=username, tweet_mode="extended")
		top = True

		for tweet in csr.items(20):
			if top:
				top_status_id = tweet.id
				top = False
			
			if tweet.id == last_status_id:
				break;

			screen_name = tweet.user.screen_name
			text = tweet.full_text
			sentiment = sentimentpy.find_sentiment(text)
			sen_list.append(sentiment)
			output.append( { 'screen_name': screen_name, 'text': text, 'sentiment': sentiment } )
			#print(tweet.full_text)

		last_status_id = top_status_id
		return output,sen_list