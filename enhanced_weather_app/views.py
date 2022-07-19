import random
import time
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.exceptions import *
import httpx
import requests
import json
import os
import re
from datetime import datetime, timezone
import pytz

from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('OPENWEATHER_API_KEY')

unit_system_names = ['imperial', 'metric']
default_unit_system = 'imperial'
default_location = 'Miami, FL, US'
# default_alert = 'No current alerts'

def default_page(request):
    units = default_unit_system
    location = request.POST.get('location', default_location)

    return render(request, 'base.html', call_api(units, location))

def call_api(unit_system, location):
    try:
        r_1 = httpx.get('http://api.openweathermap.org/geo/1.0/direct?q={0}&limit=5&appid={1}'.format(location, api_key)) 
        # weather_data_1 = json.loads(r_1.content)
        weather_data_1 = r_1.json()
        
        lat = weather_data_1[0]["lat"]
        lon = weather_data_1[0]["lon"]

        if unit_system == 'imperial':
            r_2 = httpx.get('https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=minutely&units={2}&appid={3}'.format(lat, lon, unit_system, api_key))
            degree_unit = '˚F'
            speed_unit = 'mph'
            pressure_unit  = 'mb'
            # next_speed_unit = 'km/h'
            # next_degree_unit = '˚C'
            # next_unit_system = 'metric'
            # current_unit_system = next_unit_system
        else:
            r_2 = httpx.get('https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=minutely&units=metric&appid={3}'.format(lat, lon, api_key))
            degree_unit = '˚C'
            speed_unit = 'km/h'
            pressure_unit = 'mb'
            # next_speed_unit = 'mph'
            # next_degree_unit = '˚F'
            # next_unit_system = 'imperial'
            # current_unit_system = next_unit_system

        r_3 = httpx.get('http://api.openweathermap.org/data/2.5/air_pollution?lat={0}&lon={1}&appid={2}'.format(lat, lon, api_key))

        # Full API response data
        # weather_data_2 = json.loads(r_2.content)
        weather_data_2 = r_2.json()

        # air_pollution_data = json.loads(r_3.content)
        air_pollution_data = r_3.json()

        # Current date info
        current_unix_timestamp = weather_data_2["current"]["dt"]
        current_utc_time = datetime.fromtimestamp(current_unix_timestamp, timezone.utc)
        city_timezone = pytz.timezone(weather_data_2["timezone"])
        local_time = current_utc_time.astimezone(city_timezone)
        current_date = local_time.strftime("%A %b %d, %Y").lstrip("0").replace(" 0", " ")
        current_time = local_time.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

        # Current weather info
        current_weather_icon_code = weather_data_2["current"]["weather"][0]["icon"]

        # Sunrise and sunset times
        sunrise_unix_timestamp = weather_data_2["current"]["sunrise"]
        sunrise_utc_time = datetime.fromtimestamp(sunrise_unix_timestamp, timezone.utc)
        sunrise_local_time = sunrise_utc_time.astimezone(city_timezone)
        sunrise_time = sunrise_local_time.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
        
        sunset_unix_timestamp = weather_data_2["current"]["sunset"]
        sunset_utc_time = datetime.fromtimestamp(sunset_unix_timestamp, timezone.utc)
        sunset_local_time = sunset_utc_time.astimezone(city_timezone)
        sunset_time = sunset_local_time.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

        daytime = current_unix_timestamp >= sunrise_unix_timestamp and current_unix_timestamp < sunset_unix_timestamp
        nighttime = current_unix_timestamp < sunrise_unix_timestamp and current_unix_timestamp >= sunset_unix_timestamp

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

        daily_weather_descriptions = []
        for i in range(len(daily_weather_info)):
            daily_weather_descriptions.append(daily_weather_info[i]["weather"][0]["description"])

        daily_forecast_content = zip(days_of_week, daily_weather_descriptions, daily_highs, daily_lows, daily_icon_codes)

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
        
        # Alert info
        try:
            alert_description = weather_data_2["alerts"][0]["description"]
            if alert_description == 'test for instruction':
                alert_description = 'There are no alerts'
        except:
                alert_description = "There are no alerts"

        ## Air Quality Index
        aqi = air_pollution_data["list"][0]["main"]["aqi"]

        if aqi == 1:
            air_quality_index = "Good"
        elif aqi == 2:
            air_quality_index = "Fair"
        elif aqi == 3:
            air_quality_index = "Moderate"
        elif aqi == 4:
            air_quality_index = "Poor"
        elif aqi == 5:
            air_quality_index = "Very Poor"
    except:
        invalid_input_msg = 'Location not found. Search must be in the form of "City", "City, State, Country" or "City, Country".'
        # no_alerts_msg = 'This is the exception no alerts message'
        # call_api(unit_system, default_location)
        return { 
            "invalid_input_msg": invalid_input_msg, 
            'location': default_location, 
            'current_unit_system': default_unit_system, 
            # 'no_alerts_msg': no_alerts_msg,
            # 'alert_description': no_alerts_msg
        }
    else:        
        return {
            # 'current_unit_system': current_unit_system,
            'city': weather_data_1[0]["name"],
            'current_weather': weather_data_2["current"]["weather"][0]["description"].title(),
            'lat': lat,
            'lon': lon,

            # 'current_unit_system': current_unit_system,
            'degree_unit': degree_unit,
            'speed_unit': speed_unit,
            'pressure_unit': pressure_unit,
            # 'next_unit_system': next_unit_system,
            # 'current_degree_unit': current_degree_unit,
            # 'next_degree_unit': next_degree_unit,
            # 'current_speed_unit': current_speed_unit,
            # 'next_speed_unit': next_speed_unit,

            'current_weather_icon': current_weather_icon_code,
            'current_temperature': round(weather_data_2["current"]["temp"]),
            'wind_speed': round(weather_data_2["current"]["wind_speed"]),
            'feels_like': round(weather_data_2["current"]["feels_like"]),
            'humidity': round(weather_data_2["current"]["humidity"]),
            'uv_index': round(weather_data_2["current"]["uvi"]),
            'pressure': round(weather_data_2["current"]["pressure"]),
            'chance_of_rain': round(weather_data_2["daily"][0]["pop"]*100),
            'current_date': current_date,
            'current_time': current_time,
            'sunrise_time': sunrise_time,
            'sunset_time': sunset_time,
            'daytime': daytime,
            'nighttime': nighttime,

            'days_of_week': days_of_week,
            'daily_high_temps': daily_highs,
            'daily_low_temps': daily_lows,
            'daily_weather_icons': daily_icon_codes,
            'daily_forecast_content': daily_forecast_content,

            'hours': hours,
            'hourly_temps': hourly_temps,
            'hourly_weather_icons': hourly_icon_codes,
            'hourly_forecast_content': hourly_forecast_content,

            'alert_description': alert_description,
            'air_quality_index': air_quality_index
        }

def index(request):
    return render(request, 'form.html')

def stackedareachart(request):
    """
    stackedareachart page
    """
    nb_element = 100
    xdata = range(nb_element)
    xdata = map(lambda x: 100 + x, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " balls"}}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " calls"}}

    chartdata = {
        'x': xdata,
        'name1': 'Temperature', 'y1': ydata, 'extra1': extra_serie1,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2,
    }
    charttype = "stackedAreaChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render('stackedareachart.html', data)