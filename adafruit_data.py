#install adafruit-io for aio commands to work properly
#run command: pip install adafruit-io
#github link here: https://github.com/adafruit/Adafruit_IO_Python
#adafruit.io API documentation here: https://io.adafruit.com/api/docs/#adafruit-io-http-api

import os
from Adafruit_IO import Client

#set variables for adafruit.io username and API key and create instance of REST client.
aioUsername = os.environ['adafruitAPIusername']
aioAPIkey = os.environ['adafruitAPIkey']
aio = Client(aioUsername, aioAPIkey)

#function to get zip code feed value from adafruit.io. The user can specify the zip code by typing it in on the dashboard.
def getZipCode():
  zipCode = aio.receive('zip-code-feed')
  zipCode = zipCode.value
  return zipCode

#function for posting weather data to adafruit.io 
def postData(weatherData):
  #send each of the feed values to the corresponding feed using a for loop to iterate through all the items in weatherData dictionary
  for key, value in weatherData.items():
    aio.send_data(key, value)