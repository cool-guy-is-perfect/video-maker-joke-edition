import requests
import json
from gtts import gTTS    
#gtts is imported to make audio ,because it feels good :)


data = {}
def get():
	#request joke
	url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&"
	global data
	params = {	
		"type":"twopart"
		}
	response = requests.get(url,params)
	data = response.json()
	print(data)
	delivery = data["delivery"]
	setup = data["setup"]

	#debug the text
	print("Question "+setup)
	print("Reply " +delivery)

	#convert to audio
	tts = gTTS(text = "..." + delivery, lang = 'en')
	tts.save('process/audio2.mp3')
	tts = gTTS(text = setup, lang = 'en')
	tts.save('process/audio.mp3')

