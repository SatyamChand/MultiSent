from flask import Flask, Response, url_for, request, redirect, render_template, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

# User defined imports
import text_speech_sentiment as tspy
import image_video_sentiment as ivpy
from image_video_sentiment import StreamSentiment
#from videocv2 import VideoCamera
import videocv2

UPLOAD_FOLDER = "/root/Files/Projects/MultiSent/Uploads"



app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


cont_stream=True



@app.route('/')
def index():
	return render_template('index.html')





#------------------------------------- Text and Speech --------------------------------------
sentiment=''
filename=''

@app.route('/text', methods=['GET','POST'])
def analyze_text():
	if request.method == 'POST':
		if 'textFile' not in request.files:
			file_mode = False
			inputText = request.form['inputText']
		else:
			file_mode = True
			textFile = request.files['textFile']
			if textFile == '':
				flash("No file selected", "danger")
				return redirect(request.url)
			if textFile:
				global filename
				filename = secure_filename(textFile.filename)
				print(filename)
				textFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

				with open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'r') as file:
					inputText = file.read()

		if not inputText:
			flash("Can't analyze Nothing!!", "danger")
		else:
			global sen
			sentiment = tspy.find_text_sentiment(inputText)
			print(sentiment)
			return render_template('analyze_text.html', file_mode=file_mode, filename=filename, inputText=inputText, sentiment=sentiment)
	return render_template('analyze_text.html', file_mode=False)



@app.route('/speech')
def analyze_speech():
	stt,sentiment = tspy.find_speech_sentiment()
	return render_template('analyze_speech.html', stt=stt, sentiment=sentiment)



#------------------------------------- Image and Video --------------------------------------

@app.route('/image', methods=['GET','POST'])
def analyze_image():
	if request.method == 'POST':
		if 'imageSelection' not in request.files:
			flash("No file part","danger")
			return redirect(request.url)
		imageFile = request.files['imageSelection']
		if imageFile == '' :
			flash("No file selected","danger")
			return redirect(request.url)
		if imageFile:
			global filename
			filename = secure_filename(imageFile.filename)
			imageFile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
			return render_template('analyze_image.html', image_ready=True)
	return render_template('analyze_image.html', image_ready=False)

@app.route('/image/analysis')
def imageSentiment():
	global filename
	imageFrame = ivpy.find_image_sentiment(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return Response((b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(imageFrame) + b'\r\n'), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/video', methods=['GET','POST'])
def analyze_video():
	if request.method == 'POST':
		if 'videoSelection' not in request.files:
			flash("No file part","danger")
			return redirect(request.url)
		videoFile = request.files['videoSelection']
		if videoFile == '' :
			flash("No file selected","danger")
			return redirect(request.url)
		if videoFile:
			global filename
			filename = secure_filename(videoFile.filename)
			videoFile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
			return render_template('analyze_video.html', video_ready=True)
	return render_template('analyze_video.html', video_ready=False)

@app.route('/video/vanalysis')
def videoSentiment():
	global filename
	#videoFrame = ivpy.find_video_sentiment(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return Response(ivpy.find_video_sentiment(os.path.join(app.config['UPLOAD_FOLDER'], filename)), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/video_stream')
def video_stream():
	return render_template('stream.html')

@app.route('/end_stream')
def endstream():
	global cont_stream
	print('-------------------------ended')
	ivpy.stop()
	cont_stream=False
	return "none"

@app.route('/video_stream/video_feed')
def video_feed():
	#print(dir(StreamSentiment))
	#return Response(videocv2.get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
	return Response(gen(StreamSentiment()), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(webcam):
	global cont_stream
	while cont_stream:
		frame = webcam.get_frame()
		yield frame
	cont_stream=True

#------------------------------------- Twitter---------------------------------------------

@app.route('/twitter')
def analyze_twitter():
	return render_template('analyze_twitter.html')