#openWeatherMap API documentation
#https://openweathermap.org/current
#free openWeatherMap API allows up to 60 calls a minute, but no more than 1Mil per month

import os
import datetime
import requests

#put OpenWeatherMap API key into variable called weatherAPIkey 
weatherAPIkey = os.environ['weatherAPIkey']

#big O(1)
def getOpenWeatherURL(zipCode, weatherAPIkey):
  
  #keeping country code as a variable in case I want it to be controlled via user input.
  countryCode = "US"
  #use this to get geo coordinates based on zip code. 
  geoURL = f"http://api.openweathermap.org/geo/1.0/zip?zip={zipCode},{countryCode}&appid={weatherAPIkey}"
  geoData = {}
  r = requests.get(url = geoURL)
  geoData = r.json()
  
    #build openWeatherMap API call URL using lat and lon values from the geoData dictionary we just built. 
  lat = geoData['lat']
  lon = geoData['lon']
  currentURL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={weatherAPIkey}"
  forecastURL = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=imperial&cnt=1&appid={weatherAPIkey}"
  return currentURL, forecastURL

#big O(1)
def getWeatherData(zipCode):
  #call the getOpenWeatherURL function to get the URLs we will use to get our current and forecast weather data from OpenWeatherMap
  currentWeatherURL, forecastWeatherURL = getOpenWeatherURL(zipCode, weatherAPIkey)
  #get current weather data using URL and save json data into dictionary
  currentWeatherData = {}
  r = requests.get(url = currentWeatherURL)
  currentWeatherData = r.json()
  
  #get daily weather forecast data using URL and save json data into dictionary
  forecastWeatherData = {}
  r = requests.get(url = forecastWeatherURL)
  forecastWeatherData = r.json()

  #get timezone, sunset and sunrise.
  #got help from chatGPT to get time formatted
  #use datetime and strftime to adjust sunrise and sunset to be correct for the timezone of the zip code specified
  iTimeZone = currentWeatherData['timezone']  
  iSunriseUTC = int(currentWeatherData['sys']['sunrise'] + iTimeZone)
  iSunsetUTC = int(currentWeatherData['sys']['sunset'] + iTimeZone)
  sSunrise = datetime.datetime.utcfromtimestamp(iSunriseUTC).strftime('%-I:%-M %p')
  sSunset = datetime.datetime.utcfromtimestamp(iSunsetUTC).strftime('%-I:%-M %p')
  #parse weather data and put into appropriate variables
  iTemp = int(currentWeatherData['main']['temp'])
  iHum = currentWeatherData['main']['humidity']
  sPrecip = f"{int(float(forecastWeatherData['list'][0]['pop']) * 100)}%"
  sWeatherDesc = f"{currentWeatherData['weather'][0]['description']}"
  iPressure = currentWeatherData['main']['pressure']
  
  #make a dictionary of all the data points we want to send back to adafruit with the key matching the feed key for each feed in Adafruit.io
  weatherDataDict = {
    'temp-feed': iTemp,
    'humidity-feed': iHum,
    'precipitation-feed': sPrecip,
    'description-feed': sWeatherDesc,
    'barometer-feed': iPressure,
    'sunrise-feed': sSunrise,
    'sunset-feed': sSunset
  }
  
  return weatherDataDict