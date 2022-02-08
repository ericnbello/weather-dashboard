from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.exceptions import *
import requests
import json
import os
import re
from datetime import datetime, timezone
import pytz

from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('OPENWEATHER_API_SECRET_KEY')

unit_system_names = ['imperial', 'metric']
default_unit_system = 'imperial'
default_location = 'Miami, FL, US'

def default_page(request):
    units = default_unit_system
    location = request.POST.get('location', default_location)

    return render(request, 'base.html', call_api(units, location))

def call_api(current_unit_system, location):
    try:
        r_1 = requests.get('http://api.openweathermap.org/geo/1.0/direct?q={0}&limit=5&appid={1}'.format(location, api_key)) 
        weather_data_1 = json.loads(r_1.content)
        
        lat = weather_data_1[0]["lat"]
        lon = weather_data_1[0]["lon"]

        if current_unit_system == default_unit_system:
            r_2 = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=minutely,alerts&units={2}&appid={3}'.format(lat, lon, current_unit_system, api_key))
            current_degree_unit = '˚F'
            current_speed_unit = 'mph'
            next_speed_unit = 'km/h'
            next_degree_unit = '˚C'
            next_unit_system = 'metric'
            current_unit_system = next_unit_system
        else:
            r_2 = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=minutely,alerts&units={2}&appid={3}'.format(lat, lon, current_unit_system, api_key))
            current_degree_unit = '˚C'
            current_speed_unit = 'km/h'
            next_speed_unit = 'mph'
            next_degree_unit = '˚F'
            next_unit_system = 'imperial'
            current_unit_system = next_unit_system

        # Full API response data
        weather_data_2 = json.loads(r_2.content)

        # Current date info
        current_unix_timestamp = weather_data_2["current"]["dt"]
        current_utc_time = datetime.fromtimestamp(current_unix_timestamp, timezone.utc)
        city_timezone = pytz.timezone(weather_data_2["timezone"])
        local_time = current_utc_time.astimezone(city_timezone)
        current_date = local_time.strftime("%A %b %d, %Y").lstrip("0").replace(" 0", " ")
        current_time = local_time.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

        # Current weather info
        current_weather_icon_code = weather_data_2["current"]["weather"][0]["icon"]

        # Daily weather info
        daily_weather_info = weather_data_2["daily"][1:]

        daily_dts = []
        for i in range(len(daily_weather_info)):
            daily_dts.append(daily_weather_info[i]["dt"])

        days_of_week = []
        for daily_unix_timestamp in daily_dts:
            utc_time = datetime.fromtimestamp(daily_unix_timestamp, timezone.utc)
            local_time = utc_time.astimezone()
            days_of_week.append(local_time.strftime("%A"))

        daily_highs = []
        for i in range(len(daily_weather_info)):
            daily_highs.append(round(daily_weather_info[i]["temp"]["max"]))
        
        daily_lows = []
        for i in range(len(daily_weather_info)):
            daily_lows.append(round(daily_weather_info[i]["temp"]["min"]))

        daily_icon_codes = []
        for i in range(len(daily_weather_info)):
            daily_icon_codes.append(daily_weather_info[i]["weather"][0]["icon"])

        daily_forecast_content = zip(days_of_week, daily_highs, daily_lows, daily_icon_codes)

        # Hourly weather info
        hourly_weather_info = weather_data_2["hourly"][1:]

        hourly_dts = []
        for i in range(len(hourly_weather_info)):
            hourly_dts.append(hourly_weather_info[i]["dt"])
        
        hours = []
        for hourly_unix_timestamp in hourly_dts:
            utc_time = datetime.fromtimestamp(hourly_unix_timestamp, timezone.utc)
            city_timezone = pytz.timezone(weather_data_2["timezone"])
            local_time = utc_time.astimezone(city_timezone)
            hours.append(local_time.strftime("%I%p").lstrip("0").replace(" 0", " "))
        
        hourly_temps = []
        for i in range(len(hourly_weather_info)):
            hourly_temps.append(round(hourly_weather_info[i]["temp"]))

        hourly_icon_codes = []
        for i in range(len(hourly_weather_info)):
            hourly_icon_codes.append(hourly_weather_info[i]["weather"][0]["icon"])

        hourly_forecast_content = zip(hours, hourly_temps, hourly_icon_codes)
    except:
        invalid_input_msg = 'Location not found. Search must be in the form of "City", "City, State, Country" or "City, Country".'
        return { 
            "invalid_input_msg": invalid_input_msg, 
            'location': default_location, 
            'current_unit_system': default_unit_system 
        }
    else:
        return {
            'current_unit_system': current_unit_system,
            'city': weather_data_1[0]["name"],
            'current_weather': weather_data_2["current"]["weather"][0]["description"].title(),

            'current_unit_system': current_unit_system,
            'next_unit_system': next_unit_system,
            'current_degree_unit': current_degree_unit,
            'next_degree_unit': next_degree_unit,
            'current_speed_unit': current_speed_unit,
            'next_speed_unit': next_speed_unit,

            'current_weather_icon': current_weather_icon_code,
            'current_temperature': round(weather_data_2["current"]["temp"]),
            'wind_speed': round(weather_data_2["current"]["wind_speed"]),
            'feels_like': round(weather_data_2["current"]["feels_like"]),
            'humidity': round(weather_data_2["current"]["humidity"]),
            'chance_of_rain': round(weather_data_2["daily"][0]["pop"]*100),
            'current_date': current_date,
            'current_time': current_time,

            'days_of_week': days_of_week,
            'daily_high_temps': daily_highs,
            'daily_low_temps': daily_lows,
            'daily_weather_icons': daily_icon_codes,
            'daily_forecast_content': daily_forecast_content,

            'hours': hours,
            'hourly_temps': hourly_temps,
            'hourly_weather_icons': hourly_icon_codes,
            'hourly_forecast_content': hourly_forecast_content,
        }

def index(request):
    return render(request, 'form.html')