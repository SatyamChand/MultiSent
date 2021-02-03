from fer import FER
import cv2
import numpy as np




def find_image_sentiment(path):
	image = cv2.imread(path)
	
	detector = FER()
	emotions = detector.detect_emotions(image)

	for emotion in emotions:
		(x,y,w,h) = emotion['box']
		emo = emotion['emotions']

		cv2.rectangle(image, (x, y), (x+h, y+h), (255, 0, 0), 2)
		
		sen = max(emo, key= lambda key: emo[key] )
		cv2.rectangle(image, (x, y+h-10), (x+h, y+h+30), (255, 0, 0), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(image, sen, (x, y+h+20), font, 1.0, (255, 255, 255), 1)

	image = image.copy()
	
	# cv2.imshow('outputframe',image)
	# while True:
	# 	k = cv2.waitKey(1)
	# 	if k == ord('q'):
	# 		break
	# cv2.destroyAllWindows()

	ret,imagejpg = cv2.imencode('test.jpg',image)
	#cv2.imwrite(path,imagejpg)
	return imagejpg