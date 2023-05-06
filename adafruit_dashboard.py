#install adafruit-io for aio commands to work properly
#pip install adafruit-io
#github link here: https://github.com/adafruit/Adafruit_IO_Python
#adafruit.io API documentation here: https://io.adafruit.com/api/docs/#adafruit-io-http-api

import os
import sys
from Adafruit_IO import Client
import time
import math

#set variables for adafruit.io username and API key and create instance of REST client.
aioUsername = os.environ['adafruitAPIusername']
aioAPIkey = os.environ['adafruitAPIkey']
aio = Client(aioUsername, aioAPIkey)

def getZipCode():
  #get zip code feed data from adafruit and the user can specify the zip code by typing it in on the dashboard.
  zipCode = aio.receive('zip-code-feed')
  zipCode = zipCode.value
  return zipCode

#function for posting weather data to adafruit.io 
#passing both current and forecast data, but only using current weather data for right now. 
def postData(currentWeather, forecastWeather):
  #print current and hourly weather data to the screen
  #print (currentWeather)
  #print (forecastWeather)
  #parse weather data and put into appropriate variables
  temp = int(currentWeather['main']['temp'])
  hum = currentWeather['main']['humidity']
  precip = f"{int(float(forecastWeather['list'][0]['pop']) * 100)}%"
  weatherDesc = ""
  pressure = ""
  airQuality = ""
  sunrise = ""
  sunset = ""

  #send data to corresponding adafruit.io feeds
  #aio.send_data('temp-feed', temp)
  #print(currentWeather)
  print(precip)