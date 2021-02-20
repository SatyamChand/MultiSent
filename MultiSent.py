from flask import Flask, Response, url_for, request, redirect, render_template, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

# User defined imports
from sentiment_dict import GenericSentimentCounter, MediaSentimentCounter
import text_speech_sentiment as tspy
import image_video_sentiment as ivpy
from image_video_sentiment import StreamSentiment
from twitterpy import Twitter


UPLOAD_FOLDER = "/root/Files/Projects/MultiSent/Uploads"



app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



twitter = None
cont_stream=True
media_sent_dict = MediaSentimentCounter()
global_sent_dict = GenericSentimentCounter()





@app.route('/')
def index():
	return render_template('index.html')

@app.route('/results')
def analysis_results():
	media_dict = media_sent_dict.get_dict()
	global_dict = global_sent_dict.get_agg_dict(media_dict)
	
	sent,weight = media_sent_dict.top_sentiment()
	media_sent_string = sent+' : '+weight
	sent,weight = global_sent_dict.top_sentiment(media_dict)
	global_sent_string = sent+' : '+weight

	return render_template('analysis_results.html', 
		global_sent_string=global_sent_string, media_sent_string=media_sent_string, 
		media_dict=media_dict, global_dict=global_dict)




#------------------------------------- Text and Speech --------------------------------------
sentiment=''
filename=''

@app.route('/text', methods=['GET','POST'])
def analyze_text():
	global global_sent_dict
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
			global_sent_dict.update(sentiment)
			print(sentiment)
			return render_template('analyze_text.html', file_mode=file_mode, filename=filename, inputText=inputText, sentiment=sentiment)
	return render_template('analyze_text.html', file_mode=False)




@app.route('/speech', methods=['GET','POST'])
def analyze_speech():
	global global_sent_dict
	if request.method == 'POST':
		if 'audioSelection' not in request.files:
			flash("No file part","danger")
			return redirect(request.url)

		audioFile = request.files['audioSelection']

		if audioFile == '' :
			flash("No file selected","danger")
			return redirect(request.url)

		if audioFile:
			global filename

			filename = secure_filename(audioFile.filename)
			audioFile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

			stt,sentiment = tspy.find_speech_sentiment( os.path.join(app.config["UPLOAD_FOLDER"], filename) )
			global_sent_dict.update(sentiment)
			return render_template('analyze_speech.html', speech_ready=True, stt=stt, sentiment=sentiment)

	return render_template('analyze_speech.html', speech_ready=False)





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
	imageFrame,sen = ivpy.find_image_sentiment(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	media_sent_dict.image_update(sen)
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



@app.route('/video/vanalysis')#video analysis
def videoSentiment():
	global filename, media_sent_dict
	#videoFrame = ivpy.find_video_sentiment(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return Response(ivpy.find_video_sentiment(os.path.join(app.config['UPLOAD_FOLDER'], filename), media_sent_dict ), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/video_stream')  # webcam stream analysis
def video_stream():
	return render_template('stream.html')


@app.route('/video_stream/video_feed')
def video_feed():
	return Response(gen(StreamSentiment()), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(webcam):
	global cont_stream,media_sent_dict
	while cont_stream:
		frame,sent = webcam.get_frame()
		media_sent_dict.video_update(sent)
		yield frame
	cont_stream=True




@app.route('/end_stream')		#function to stop analysis of videos
def endstream():
	global cont_stream
	ivpy.stop()
	cont_stream=False
	return "none"




#------------------------------------- Twitter---------------------------------------------

@app.route('/twitter_test')
def twitter_test():
	global twitter,global_sent_dict
	if twitter == None:
		twitter = Twitter()
	tweets,sen_list = twitter.get_mentions_with_cursor('@elonmusk')
	global_sent_dict.update_from_list(sen_list)
	if len(tweets)==0:
		print('No new tweet')
		return render_template('twitter_test.html', no_new_tweet=True)
	#return render_template('twitter.html', home_user=home_user, tweets=tweets)
	print('New tweet(s)')
	return render_template('twitter_test.html', no_new_tweet=False, tweets=tweets)



@app.route('/twitter')
def analyze_twitter():
	global twitter, global_sent_dict
	if twitter == None:
		twitter = Twitter()
	tweets,sen_list = twitter.get_tweets_for_page('@elonmusk')
	global_sent_dict.update_from_list(sen_list)
	return render_template('analyze_twitter.html', tweets=tweets)