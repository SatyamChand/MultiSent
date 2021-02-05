import cv2
from imutils.video import WebcamVideoStream

class VideoCamera:

	def __init__(self):
		self.stream = WebcamVideoStream(src=0).start()

	def __del__(self):
		self.stream.release()

	def get_frame(self):

		frame = self.stream.read()
		frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
		ret,image = cv2.imencode('.jpg', frame)

		data = []
		data.append(image.tobytes())		#byte fromat for global server, no issues with direct image on local server
		return data