from __future__ import unicode_literals
import sys
import youtube_dl
import os
import simpleaudio as sa

if len(sys.argv) == 2:
    youtubeUrl = str(sys.argv[1])

song_there = os.path.isfile("song.wav")
print(youtubeUrl)

try:
	if song_there:
		os.remove("song.wav")
		print("Файл удалён")
except PermissionError:
	print("Не удалось удалить файл")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',#mp3
        'preferredquality': '192',
    }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	ydl.download([youtubeUrl])

for file in os.listdir('./'):
	if file.endswith('.wav'):
		print(f'+ {file}')
		os.rename(file, 'song.wav')

print("Проигрываю музыку")

wave_obj = sa.WaveObject.from_wave_file('song.wav')
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing