from fer import FER
import cv2
import numpy as np



cont_stream=True


def find_image_sentiment(path):
	frame = cv2.imread(path)
	height = frame.shape[0]
	size_factor = 700/height;
	image = cv2.resize(frame, (0,0), fx=size_factor, fy=size_factor)
	

	detector = FER()
	emotions = detector.detect_emotions(image)
	top_sen = None
	for emotion in emotions:
		(x,y,w,h) = emotion['box']
		emo = emotion['emotions']

		cv2.rectangle(image, (x, y), (x+h, y+h), (255, 0, 0), 1)
		
		sen = max(emo, key= lambda key: emo[key] )
		if top_sen == None:
			top_sen = sen
		cv2.rectangle(image, (x, y+h-10), (x+h, y+h+30), (255, 0, 0), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(image, sen, (x, y+h+20), font, 0.75, (255, 255, 255), 1)
	
	# cv2.imshow('outputframe',image)
	# while True:
	# 	k = cv2.waitKey(1)
	# 	if k == ord('q'):
	# 		break
	# cv2.destroyAllWindows()

	ret,imagejpg = cv2.imencode('test.jpg',image)
	return imagejpg,top_sen

class StreamSentiment:
	def __init__(self):
		self.videocam = cv2.VideoCapture(0)
		self.detector = FER()

	def __del__(self):
		print('videocam released------------------------------------------------')
		self.videocam.release()
		#cv2.destroyAllWindows()

	def get_frames(self):
		frame_counter=True

		while True:
			ret,frame = self.videocam.read()
			frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

			if frame_counter == True:

				emotions = self.detector.detect_emotions(frame)

			for emotion in emotions:
				(x,y,w,h) = emotion['box']
				emo = emotion['emotions']

				cv2.rectangle(frame, (x, y), (x+h, y+h), (255, 0, 0), 1)
				
				sen = max(emo, key= lambda key: emo[key] )
				cv2.rectangle(frame, (x, y+h-10), (x+h, y+h+30), (255, 0, 0), cv2.FILLED)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, sen, (x, y+h+20), font, 0.75, (255, 255, 255), 1)

			ret,image = cv2.imencode('.jpg', frame)
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(image) + b'\r\n')

			frame_counter = not frame_counter
		print('get_frame() ended')

	def get_frame(self):
		ret,frame = self.videocam.read()
		#frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

		sen='neutral'
		emotions = self.detector.detect_emotions(frame)
		top_sen = None
		for emotion in emotions:
			(x,y,w,h) = emotion['box']
			emo = emotion['emotions']

			cv2.rectangle(frame, (x, y), (x+h, y+h), (255, 0, 0), 1)
			
			sen = max(emo, key= lambda key: emo[key] )
			if top_sen == None :
				top_sen = sen
			cv2.rectangle(frame, (x, y+h-10), (x+h, y+h+30), (255, 0, 0), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, sen, (x, y+h+20), font, 0.75, (255, 255, 255), 1)

		ret,image = cv2.imencode('.jpg', frame)
		return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(image) + b'\r\n'),top_sen


def find_video_sentiment(path,media_sent_dict):
	global cont_stream
	print(path)
	videocam = cv2.VideoCapture(path)
	detector = FER()

	frame_counter=True

	while cont_stream:
		#print(cont_stream)
		ret,frame = videocam.read()
		frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
		top_sen = None

		if frame_counter == True:

			emotions = detector.detect_emotions(frame)

		for emotion in emotions:
			(x,y,w,h) = emotion['box']
			emo = emotion['emotions']

			cv2.rectangle(frame, (x, y), (x+h, y+h), (255, 0, 0), 1)
			
			sen = max(emo, key= lambda key: emo[key] )
			media_sent_dict.video_update(sen)
			if top_sen == None:
				top_sen = sen
			cv2.rectangle(frame, (x, y+h-10), (x+h, y+h+30), (255, 0, 0), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, sen, (x, y+h+20), font, 0.75, (255, 255, 255), 1)

		ret,image = cv2.imencode('.jpg', frame)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(image) + b'\r\n')

		frame_counter = not frame_counter

	cont_stream = True
	print('video ended')
	videocam.release()
	#cv2.destroyAllWindows()

def stop():
	global cont_stream
	#print('changed')
	cont_stream = False