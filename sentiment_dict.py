#from datetime import datetime, timedelta


class GenericSentimentCounter:
	def __init__(self):
		self.isEmpty = True
		self.positive_list = ['happy', 'surprise']
		self.negative_list = ['angry', 'disgust', 'fear', 'sad']
		self.sent_dict = { 'Positive': 0, 'Neutral':0, 'Negative': 0 }



	def update(self, key):
		self.sent_dict[key] += 1
		self.isEmpty = False



	def update_from_list(self, sent_list):
		for key in sent_list:
			self.sent_dict[key] += 1
		self.isEmpty = False



	def top_sentiment(self, media_dict):
		if self.isEmpty == True:
			return 'No evaluation done', '0.00'

		#top_sen = max(self.sent_dict, key= lambda key: self.sent_dict[key] )
		count = 0
		top_sen = ''
		max_sen = -1
		agg_dict = self.get_agg_dict( media_dict )
		for key,val in agg_dict.items():
			if max_sen < val:
				max_sen = val
				top_sen = key
			count += val
		return top_sen, '{:0.2f}'.format(max_sen/count)



	def get_dict(self):
		return self.sent_dict



	def get_agg_dict(self, media_dict):
		temp_dict = self.sent_dict.copy()
		
		for key in media_dict:
			if key in self.positive_list:
				temp_dict['Positive'] += (media_dict[key]//100)

			elif key in self.negative_list:
				temp_dict['Negative'] += (media_dict[key]//100)

			else:
				temp_dict['Neutral'] += (media_dict[key]//100)
		
		return temp_dict





class MediaSentimentCounter:
	def __init__(self):
		self.n = 0
		self.sent_dict = { 'happy': 0, 'surprise': 0, 'neutral': 0, 'angry': 0, 'disgust': 0, 'fear': 0, 'sad': 0 }
		#self.delta = timedelta(seconds=10)     #can be used in time based increments



	def video_update(self, key):
		if key == None:
			return
		self.sent_dict[key] += 1
		self.n += 1



	def image_update(self, key):
		self.sent_dict[key] += 100
		self.n += 100



	def top_sentiment(self):
		if self.n == 0:
			return 'No evaluation done', '0.00'

		top_sen = max(self.sent_dict, key= lambda key: self.sent_dict[key] )
		return top_sen, '{:0.2f}'.format(self.sent_dict[top_sen]/self.n)


	def get_dict(self):
		return self.sent_dict