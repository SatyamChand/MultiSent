import cv2

def get_frames():
	videocam = cv2.VideoCapture(0)

	while True:
		ret,frame = videocam.read()
		frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

		ret,image = cv2.imencode('.jpg', frame)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(image) + b'\r\n')

	videocam.release()
	cv2.destroyAllWindows()