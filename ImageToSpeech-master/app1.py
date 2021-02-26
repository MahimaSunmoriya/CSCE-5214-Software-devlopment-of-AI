#!flask/bin/python
from flask import Flask, render_template
import cv2
import imutils
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
import time
from base64 import b64encode
from IPython.display import Image
from pylab import rcParams
rcParams['figure.figsize'] = 10, 20
import sqlite3

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "vision_api.json"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/con')
def convertor():

# Extract text from image
	from google.cloud import vision
	import io
	client = vision.ImageAnnotatorClient()
	file_name = os.path.abspath('Image1.jpg')
	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = vision.Image(content=content)

	response = client.text_detection(image=image)
	texts = response.text_annotations
	# print('Texts:',texts[0].description)
	print(len(texts[0].description))

	# for text in texts:
	# 	result='\n"{}"'.format(text.description)
	# 	print("My",result)

	#     vertices = (['({},{})'.format(vertex.x, vertex.y)
	#                 for vertex in text.bounding_poly.vertices])

	#     print('bounds: {}'.format(','.join(vertices)))
	#     # return '\n"{}"'.format(text.description)

	if response.error.message:
	    raise Exception(
	        '{}\nFor more info on error messages, check: '
	        'https://cloud.google.com/apis/design/errors'.format(
	            response.error.message))
	from google.cloud import texttospeech


## Synthesizes speech from the input string of text
	# Instantiates a client
	client = texttospeech.TextToSpeechClient()

	# Set the text input to be synthesized
	synthesis_input = texttospeech.SynthesisInput(text=texts[0].description)

	# Build the voice request, select the language code ("en-US") and the ssml
	# voice gender ("neutral")
	voice = texttospeech.VoiceSelectionParams(
	    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
	)

	# Select the type of audio file you want returned
	audio_config = texttospeech.AudioConfig(
	    audio_encoding=texttospeech.AudioEncoding.MP3
	)

	# Perform the text-to-speech request on the text input with the selected
	# voice parameters and audio file type
	response = client.synthesize_speech(
	    input=synthesis_input, voice=voice, audio_config=audio_config
	)

	# The response's audio_content is binary.
	with open("output.mp3", "wb") as out:
	    # Write the response to the output file.
	    out.write(response.audio_content)
	    print('Audio content written to file "output.mp3"')



	from google.cloud import speech
	client = speech.SpeechClient()

	audio = speech.RecognitionAudio(uri="output.mp3")
	config = speech.RecognitionConfig(
	    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
	    sample_rate_hertz=16000,
	    language_code="en-US",
	    enable_word_time_offsets=True,
	)

	operation = client.long_running_recognize(config=config, audio=audio)

	print("Waiting for operation to complete...")
	result = operation.result(timeout=90)

	for result in result.results:
	    alternative = result.alternatives[0]
	    print("Transcript: {}".format(alternative.transcript))
	    print("Confidence: {}".format(alternative.confidence))

	    for word_info in alternative.words:
	        word = word_info.word
	        start_time = word_info.start_time
	        end_time = word_info.end_time

	        print(
	            f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
	        )





	return '\n"{}"'.format(texts[0].description)
	# return "Done"

# from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = '/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# from flask import send_from_directory
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)



def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index')
def index():
    return render_template('index.html')
if __name__ == '__main__':
	app.run(host="localhost",port="8000",debug=True)
