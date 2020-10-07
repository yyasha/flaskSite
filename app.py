from flask import Flask, render_template, url_for, send_file, request
from flask_socketio import SocketIO
import requests, json
from threading import Thread
import time
import urllib.request
from xml.dom import minidom
import os
import subprocess
import sys

esp8266LedstreepIP = '192.168.1.9'

temp = '-'
feels = '-'
humidity = '-'
windSpeed = '-'
cloudsG = '-'
rainG = '-'
snowG = '-'

USD = ' '
EUR = ' '
AUD = ' '
GBP = ' '
BYN = ' '
HKD = ' '
KZT = ' '
CAD = ' '
CNY = ' '
NOK = ' '
SGD = ' '
TRY = ' '
UAH = ' '
CZK = ' '
SEK = ' '
CHF = ' '
JPY = ' '
youtubeUrl = 'url'

runCur = True               #Потоки
runWeather = True
runSound = False
stopSound = False

app = Flask(__name__)
socketio = SocketIO(app)

def mainThread():
	@app.route('/')
	def index():
		return render_template("index.html")

	@app.route('/ledstreep')
	def ledstreep():
		return render_template("ledstreep.html")

	@app.route('/currencies')
	def currencies():
		return render_template("currencies.html")

	@app.route('/weather')
	def weather():
		return render_template("weather.html")

	@app.route('/sound', methods=['post', 'get'])
	def sound():
		if request.method == 'POST':
			url = request.form.get('username')     # запрос к данным формы 
			speaker = request.form.get('speaker')

			if url != '':
				# os.system(f'python3 sound.py {youtubeUrl}')
				global youtubeUrl
				youtubeUrl = url
				global runSound
				runSound = True

			if speaker != '':
				os.system(f"amixer cset numid=1 -- {speaker}")

		return render_template("sound.html")

	@app.route('/stopSound')
	def stopSound():
		global stopSound
		stopSound = True
		return("stopped")
	 
	@app.route('/images/<filename>')
	def get_image(filename):
		return send_file('images/' + filename)
	 
	@app.route('/mode0')
	def mode0():
		requests.get(f'http://{esp8266LedstreepIP}/mode0')
		return 'mode0'
	 
	@app.route('/mode1')
	def mode1():
		requests.get(f'http://{esp8266LedstreepIP}/mode1')
		return 'modeChange'

	@app.route('/mode2')
	def mode2():
		requests.get(f'http://{esp8266LedstreepIP}/mode2')
		return 'modeChange'

	@app.route('/mode3')
	def mode3():
		requests.get(f'http://{esp8266LedstreepIP}/mode3')
		return 'modeChange'

	@app.route('/mode5')
	def mode5():
		requests.get(f'http://{esp8266LedstreepIP}/mode5')
		return 'modeChange'

	@app.route('/mode11')
	def mode11():
		requests.get(f'http://{esp8266LedstreepIP}/mode11')
		return 'modeChange'

	@app.route('/mode12')
	def mode12():
		requests.get(f'http://{esp8266LedstreepIP}/mode12')
		return 'modeChange'

	@app.route('/mode13')
	def mode13():
		requests.get(f'http://{esp8266LedstreepIP}/mode13')
		return 'modeChange'

	@app.route('/mode14')
	def mode14():
		requests.get(f'http://{esp8266LedstreepIP}/mode14')
		return 'modeChange'

	@app.route('/mode15')
	def mode15():
		requests.get(f'http://{esp8266LedstreepIP}/mode15')
		return 'modeChange'

	@app.route('/mode16')
	def mode16():
		requests.get(f'http://{esp8266LedstreepIP}/mode16')
		return 'modeChange'

	@app.route('/mode17')
	def mode17():
		requests.get(f'http://{esp8266LedstreepIP}/mode17')
		return 'modeChange'

	@app.route('/mode18')
	def mode18():
		requests.get(f'http://{esp8266LedstreepIP}/mode18')
		return 'modeChange'

	@app.route('/mode19')
	def mode19():
		requests.get(f'http://{esp8266LedstreepIP}/mode19')
		return 'modeChange'

	@app.route('/mode20')
	def mode20():
		requests.get(f'http://{esp8266LedstreepIP}/mode20')
		return 'modeChange'

	@socketio.on('currencies')
	def checkMessage(run):
		global AUD
		global GBP
		global BYN
		global HKD
		global USD
		global EUR
		global KZT
		global CAD
		global CNY
		global NOK
		global SGD
		global TRY
		global UAH
		global CZK
		global SEK
		global CHF
		global JPY
		global runCur
		runCur = True
		socketio.emit('AUD', AUD)
		socketio.emit('GBP', GBP)
		socketio.emit('BYN', BYN)
		socketio.emit('HKD', HKD)
		socketio.emit('USD', USD)
		socketio.emit('EUR', EUR)
		socketio.emit('KZT', KZT)
		socketio.emit('CAD', CAD)
		socketio.emit('CNY', CNY)
		socketio.emit('NOK', NOK)
		socketio.emit('SGD', SGD)
		socketio.emit('TRY', TRY)
		socketio.emit('UAH', UAH)
		socketio.emit('CZK', CZK)
		socketio.emit('SEK', SEK)
		socketio.emit('CHF', CHF)
		socketio.emit('JPY', JPY)

	@socketio.on('weather')
	def checkWeather(run):
		global runWeather
		runWeather = True
		socketio.emit('temperature', f'{temp}°C')
		socketio.emit('feels', f'{feels}°C')
		socketio.emit('humidity', f'{humidity}%')
		socketio.emit('wind', f'{windSpeed} м/с')
		socketio.emit('clouds', f'{cloudsG}%')
		socketio.emit('rain', f'{rainG} mm')
		socketio.emit('snow', f'{snowG} mm')

def weatherw():
	while True:
		global runWeather
		global temp
		global feels
		global windSpeed
		global humidity
		if runWeather == True:
			runWeather = False
			print('worker Weather')
			url = "http://api.openweathermap.org/data/2.5/forecast"
			payload = {
			    "lat": "48.704250",
			    "lon": "44.465634",
			    "units": "metric",
			    "appid": "YourKey",
			}
			res = requests.get(url, params=payload)
			data = json.loads(res.text)
				
			weather = data["list"][0]
			global temp
			global feels
			global windSpeed
			global humidity
				
			def pars_weather(weatherType, timeRange, measurementUnits):

				global cloudsG
				global rainG
				global snowG

				if (weatherType in weather) and (timeRange in weather[weatherType].keys()):
					if weatherType == 'clouds':
						cloudsG = weather[weatherType][timeRange]
					elif weatherType == 'rain':
						rainG = weather[weatherType][timeRange]
					elif weatherType == 'snow':
						snowG = weather[weatherType][timeRange]
				else:
					if weatherType == 'clouds':
						cloudsG = "none"
					elif weatherType == 'rain':
						rainG = "none"
					elif weatherType == 'snow':
						snowG = "none"

			pars_weather("clouds", "all", "%")
			pars_weather("rain", "1h", "mm")
			pars_weather("snow", "1h", "mm")
			temp = weather["main"]["temp"]
			feels = weather["main"]["feels_like"]
			windSpeed = weather['wind']['speed']
			humidity = weather["main"]['humidity']


def currency():
	while True:
		global runCur
		if runCur == True:
			runCur = False
			print('worker USD')
			global AUD
			global GBP
			global BYN
			global HKD
			global USD
			global EUR
			global KZT
			global CAD
			global CNY
			global NOK
			global SGD
			global TRY
			global UAH
			global CZK
			global SEK
			global CHF
			global JPY
			url = "http://www.cbr.ru/scripts/XML_daily.asp"

			web = urllib.request.urlopen(url)
			data = web.read()

			UrlSplit = url.split("/")[-1]
			ExtSplit = UrlSplit.split(".")[1]
			FileName = UrlSplit.replace(ExtSplit, "xml")

			with open(FileName, "wb") as localFile:
			    localFile.write(data)

			doc = minidom.parse(FileName)

			currency = doc.getElementsByTagName("Valute")

			for rate in currency:
			    name = rate.getElementsByTagName("Name")[0]
			    value = rate.getElementsByTagName("Value")[0]
			    name = name.firstChild.data
			    value = value.firstChild.data

			    if name == 'Австралийский доллар':
			        global AUD
			        AUD = value
			    elif name == 'Фунт стерлингов Соединенного королевства':
			        global GBP
			        GBP = value
			    elif name == 'Белорусский рубль':
			        global BYN
			        BYN = value
			    elif name == 'Гонконгских долларов':
			        global HKD
			        HKD = value
			    elif name == 'Доллар США':
			        global USD
			        USD = value
			    elif name == 'Евро':
			        global EUR
			        EUR = value
			    elif name == 'Казахстанских тенге':
			        global KZT
			        KZT = value
			    elif name == 'Канадский доллар':
			        global CAD
			        CAD = value
			    elif name == 'Китайских юаней':
			        global CNY
			        CNY = value
			    elif name == 'Норвежских крон':
			        global NOK
			        NOK = value
			    elif name == 'Сингапурский доллар':
			        global SGD
			        SGD = value
			    elif name == 'Турецкая лира':
			        global TRY
			        TRY = value
			    elif name == 'Украинских гривен':
			        global UAH
			        UAH = value
			    elif name == 'Чешских крон':
			        global CZK
			        CZK = value
			    elif name == 'Шведских крон':
			        global SEK
			        SEK = value
			    elif name == 'Швейцарский франк':
			        global CHF
			        CHF = value
			    elif name == 'Японских иен':
			        global JPY
			        JPY = value
		time.sleep(60)

def sound():
	while True:
		global runSound
		global stopSound
		if runSound == True:
			runSound = False
			global youtubeUrl
			# os.system(f'python3 sound.py {youtubeUrl}')
			playSound = subprocess.Popen([sys.executable, "sound.py", f"{youtubeUrl}"])
			time.sleep(20)
		if stopSound == True:
			print("Stopping")
			try:
				playSound.terminate()
				print("Stopped")
			except Exception as e:
				print("error")

			stopSound = False

threadMain = Thread(target=mainThread)
threadWeather = Thread(target=weatherw)
threadCur = Thread(target=currency)
threadSound = Thread(target=sound)

threadMain.start()
threadWeather.start()
threadCur.start()
threadSound.start()

if __name__ == "__main__":
	socketio.run(app, debug=True, port=8080, host='0.0.0.0')
