#openWeatherMap API documentation
#https://openweathermap.org/current
#free openWeatherMap API allows up to 60 calls a minute, but no more than 1Mil per month

import os
import sys
import datetime
import pytz
import json
import requests
import time

#used this for testing. 
#zipCode = input("Zip Code: ")

#get zip code feed data from adafruit and the user can specify the zip code by typing it in on the dashboard
#zipCode = aio.receive(zipCodeFeed)
#zipCode = zipCode.value

#put OpenWeatherMap API key into variable called weatherAPIkey 
weatherAPIkey = os.environ['weatherAPIkey']

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
  return currentWeatherData, forecastWeatherData 