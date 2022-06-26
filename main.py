import random
import ffmpeg
import os
import goke_gen as test
import json
class create:
	def __init__(self,img):
		self.test = test
		self.img = img
		self.start = 0
		self.end = 0
		self.iterator1 = 1
	def createAudio(self,aud1,aud2):
		self.test.get()
		self.audio_1 = aud1
		self.audio_2 = aud2
		self.test = test
	def createText(self):
 		self.subtitle = ""
 		self.quote = [test.data["setup"],"Reply: "+test.data["delivery"]]
 		for self.i in self.quote:
 			if len(str(self.start)) == 1:
 				self.start = f"0{self.start}"
 			if len(str(self.end)) == 1:
 				self.end = f"0{self.end}"
 			s = f"""{self.iterator1}
00:00:{self.start},000 --> 00:00:{self.end},000
{self.i}
"""
 			self.subtitle = self.subtitle + s
 			self.start = int(self.start)
 			self.end = int(self.end)
 			self.start = self.end
 			self.end = self.end + self.duration_aud_2 +1
 			self.iterator1 += 1
 		self.file = open("subtitle.srt", "r+")
 		self.file.truncate(0)
 		self.file.write(self.subtitle)
 		self.file.close() #to change file access modes
	def preProduce(self):
		self.input_aud_1 = ffmpeg.probe(f"process/{self.audio_1}")
		self.input_aud_2 = ffmpeg.probe(f"process/{self.audio_2}")
		self.duration_aud_1 = self.input_aud_1['format']['duration']
		self.duration_aud_1 = float(self.duration_aud_1)
		self.duration_aud_1 = int(self.duration_aud_1)
		self.duration_aud_2 = self.input_aud_2['format']['duration']
		self.duration_aud_2 = float(self.duration_aud_2)
		self.duration_aud_2 = int(self.duration_aud_2)
		print(self.duration_aud_2 + self.duration_aud_1)


		#change some
		self.end = self.duration_aud_1
	def createFile(self):
		# create a file
		os.system(f"""ffmpeg -loop 1 -y -i input/{self.img} -c:v libx264 -t {self.duration_aud_2 + self.duration_aud_1 + 1} -pix_fmt yuv420p -vf scale=1080:1920 process/out-beta.mp4""")
		# apply overlay
		os.system(f"""ffmpeg -y -i process/out-beta.mp4 -i additional/overlay.png -filter_complex "[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable='between(t,0,20)'" -pix_fmt yuv420p -c:a copy process/out-cache.mp4""")
		# combine audio
		os.system(f"""ffmpeg -y -i "concat:process/{self.audio_1}|process/{self.audio_2}" -acodec copy process/audio-out.mp3""")
		# add text
		os.system(f"""ffmpeg -y -i process/out-cache.mp4 -vf "subtitles=subtitle.srt:force_style='Alignment=10,Fontsize=18,PrimaryColour=&H0xFAEBD7&,FontName=DejaVu Serif'" -c:a copy process/out-beta.mp4""")
		# add audio
		os.system(f"""ffmpeg -y -i process/out-beta.mp4 -i process/audio-out.mp3 -map 0 -map 1:a -c:v copy -shortest out-main.mp4""")
def generate():

	n = 1 #random.randint(0,4)
	video = create(f"input.jpg")#add n to get a random image from input folder
	video.createAudio("audio.mp3","audio2.mp3")
	video.preProduce()
	video.createText()
	video.createFile()

generate()
