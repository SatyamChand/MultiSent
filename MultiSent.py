from flask import Flask, Response, url_for, request, redirect, render_template, flash, send_from_directory
import os
from werkzeug.utils import secure_filename


# User defined imports
import text_speech_recognition as tspy


UPLOAD_FOLDER = "/root/Files/Projects/MultiSent/Uploads"



app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

@app.route('/image')
def analyze_image():
	return render_template('analyze_image.html')



@app.route('/video')
def analyze_video():
	return render_template('analyze_video.html')



#------------------------------------- Twitter---------------------------------------------

@app.route('/twitter')
def analyze_twitter():
	return render_template('analyze_twitter.html')