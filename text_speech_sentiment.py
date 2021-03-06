import speech_recognition as sr
import sentimentpy

def find_text_sentiment(text):
	return sentimentpy.find_sentiment(text)
	

def find_speech_sentiment(path):			#currently utilizes a file for recognition
	recognizer = sr.Recognizer()
	print('in sr')
	with sr.WavFile(path) as file:
		audio = recognizer.record(file)

	try:
		stt = recognizer.recognize_google(audio, language = 'en-US')
		print("Speech: " + stt)
	except LookupError:
		print("Could not understand audio")

	print('finding sentiment')
	sentiment = sentimentpy.find_sentiment(stt)
	print('sentiment : ',sentiment)
	return stt,sentiment