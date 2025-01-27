import random
import time
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.exceptions import *
import httpx
import requests
import json
import os
# import re
from datetime import datetime, timezone
import pytz

from dotenv import load_dotenv
load_dotenv()

# openweather_api_key = ''
openweather_api_key = os.environ.get('OPENWEATHER_API_KEY')

unit_system_names = ['imperial', 'metric']
default_unit_system = 'imperial'
default_location = 'Miami, FL, US'
# default_alert = 'No current alerts'

def default_page(request):
    units = default_unit_system
    location = request.POST.get('location', default_location)

    return render(request, '../templates/base.html', call_api(units, location))

def call_api(unit_system, location):
    try:
        # r_1 = httpx.get('http://api.openweathermap.org/geo/1.0/direct?q={0}&limit=5&appid={1}'.format(location, openweather_api_key))
        # weather_data_1 = r_1.json()

        r_1 = requests.get('http://api.openweathermap.org/geo/1.0/direct?q={0}&limit=5&appid={1}'.format(location, openweather_api_key)) 
        weather_data_1 = json.loads(r_1.text)
        
        lat = weather_data_1[0]["lat"]
        lon = weather_data_1[0]["lon"]

        if unit_system == 'imperial':
            r_2 = requests.get('https://api.openweathermap.org/data/3.0/onecall?lat={0}&lon={1}&units={2}&exclude=minutely&appid={3}'.format(lat, lon, unit_system, openweather_api_key))
            # r_2 = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=minutely&units={2}&appid={3}'.format(lat, lon, unit_system, openweather_api_key))
            degree_unit = '˚F'
            speed_unit = 'mph'
            pressure_unit  = 'mb'
            # next_speed_unit = 'km/h'
            # next_degree_unit = '˚C'
            # next_unit_system = 'metric'
            # current_unit_system = next_unit_system
        else:
            r_2 = requests.get('https://api.openweathermap.org/data/3.0/onecall?lat={0}&lon={1}&exclude={minutely}&units={2}&appid={3}'.format(lat, lon, unit_system, openweather_api_key))
            # r_2 = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=minutely&units=metric&appid={3}'.format(lat, lon, openweather_api_key))
            degree_unit = '˚C'
            speed_unit = 'km/h'
            pressure_unit = 'mb'
            # next_speed_unit = 'mph'
            # next_degree_unit = '˚F'
            # next_unit_system = 'imperial'
            # current_unit_system = next_unit_system

        r_3 = requests.get('http://api.openweathermap.org/data/2.5/air_pollution?lat={0}&lon={1}&appid={2}'.format(lat, lon, openweather_api_key))

        # Full API response data
        # weather_data_2 = json.loads(r_2.content)
        weather_data_2 = r_2.json()

        air_pollution_data = json.loads(r_3.content)
        air_pollution_data = r_3.json()

        # Current date info
        current_unix_timestamp = weather_data_2["current"]["dt"]
        current_utc_time = datetime.fromtimestamp(current_unix_timestamp, timezone.utc)
        city_timezone = pytz.timezone(weather_data_2["timezone"])
        local_time = current_utc_time.astimezone(city_timezone)
        # Full day name, i.e. Sunday
        # current_date_full_day_name = local_time.strftime("%A %b %d, %Y").lstrip("0").replace(" 0", " ")
        # Abbreviated day name, i.e. Sun
        current_date = local_time.strftime("%a %b %d, %Y").lstrip("0").replace(" 0", " ")

        current_time = local_time.strftime("%I:%M %p").lstrip("0").replace(" 0", " ").lower()

        # Current weather info
        current_weather_summary = weather_data_2["daily"][0]["summary"]
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

        # Today's moonrise time
        todays_moonrise_dt = []
        for i in range(len(daily_weather_info)):
            todays_moonrise_dt.append(daily_weather_info[0]["moonrise"])

        todays_moonrise_time = []
        for unix_timestamp in todays_moonrise_dt:
            utc_time = datetime.fromtimestamp(unix_timestamp, timezone.utc)
            local_time = utc_time.astimezone()
            todays_moonrise_time.append(local_time.strftime("%-I:%M %p").lower())

        # Daily moonrise time starting 'tomorrow'
        daily_moonrise_dts = []
        for i in range(len(daily_weather_info)):
            daily_moonrise_dts.append(daily_weather_info[i]["moonrise"])

        daily_moonrise_times = []
        for daily_unix_timestamp in daily_moonrise_dts:
            utc_time = datetime.fromtimestamp(daily_unix_timestamp, timezone.utc)
            local_time = utc_time.astimezone()
            daily_moonrise_times.append(local_time.strftime("%-I:%M %p").lower())

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

        
        # for i in range(len(daily_weather_info)):
            # daily_moonrise_times.append(daily_weather_info[i]["moonrise"])

        daily_forecast_content = zip(days_of_week, daily_weather_descriptions, daily_highs, daily_lows, daily_icon_codes, daily_moonrise_times)

        daily_forecast_content_list = list(daily_forecast_content)

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

        hourly_wind_speeds = []
        for i in range(len(hourly_weather_info)):
            hourly_wind_speeds.append(round(hourly_weather_info[i]["wind_speed"]))
        
        hourly_humidity = []
        for i in range(len(hourly_weather_info)):
            hourly_humidity.append(round(hourly_weather_info[i]["humidity"]))

        # hourly_rainfall = []
        # for i in range(len(hourly_weather_info)):
        #     hourly_rainfall.append(round(hourly_weather_info[i]["rain"]))

        hourly_icon_codes = []
        for i in range(len(hourly_weather_info)):
            hourly_icon_codes.append(hourly_weather_info[i]["weather"][0]["icon"])
        
        hourly_weather_descriptions = []
        for i in range(len(hourly_weather_info)):
            hourly_weather_descriptions.append(hourly_weather_info[i]["weather"][0]["description"])

        hourly_forecast_content = zip(hours, hourly_temps, hourly_icon_codes, hourly_weather_descriptions)

        hourly_forecast_content_list = list(hourly_forecast_content)
        
        # Alert info
        try:
            alert_description = weather_data_2["alerts"][0]["description"]
            if alert_description == 'test for instruction':
                alert_description = 'There are no alerts'
        except:
                alert_description = "There are no alerts"

        ## Air Quality Index
        aqi_values = air_pollution_data["list"][0]["main"]["aqi"]

        # if aqi == 1:
        #     air_quality_index = "Good"
        # elif aqi == 2:
        #     air_quality_index = "Fair"
        # elif aqi == 3:
        #     air_quality_index = "Moderate"
        # elif aqi == 4:
        #     air_quality_index = "Poor"
        # elif aqi == 5:
        #     air_quality_index = "Very Poor"

        # Air pressure info
        air_pressure = round(weather_data_2["current"]["pressure"])

        hourly_air_pressures = []
        for i in range(len(weather_data_2["hourly"])):
            hourly_air_pressures.append(weather_data_2["hourly"][i]["pressure"])
        
        todays_avg_air_pressure = round(sum(hourly_air_pressures)/len(hourly_air_pressures))


        ## UV Index Info
        uv_index = round(weather_data_2["current"]["uvi"])

        if uv_index <= 2:
            uv_index_meaning = "Low"
        elif uv_index <= 5:
            uv_index_meaning = "Moderate"
        elif uv_index <= 7:
            uv_index_meaning = "High"
        elif uv_index <= 10:
            uv_index_meaning = "Very High"
        else:
            uv_index_meaning = "Extreme"

        # Moon Phase Info
        current_moon_phase_value = weather_data_2["daily"][0]["moon_phase"]
        
        # List of icons without "alt" entries
        moon_phase_mappings = {
            "New Moon": ("wi-moon-new", "f095"),
            "Waxing Crescent": ("wi-moon-waxing-crescent-1", "f096"),
            "First Quarter": ("wi-moon-first-quarter", "f09c"),
            "Waxing Gibbous": ("wi-moon-waxing-gibbous-1", "f09d"),
            "Full Moon": ("wi-moon-full", "f0a3"),
            "Waning Gibbous": ("wi-moon-waning-gibbous-1", "f0a4"),
            "Last Quarter": ("wi-moon-third-quarter", "f0aa"),
            "Waning Crescent": ("wi-moon-waning-crescent-1", "f0ab")
        }

        # Mapping moon phase value to names
        if current_moon_phase_value == 0:
            current_moon_phase = "New Moon"
        elif current_moon_phase_value == 0.25:
            current_moon_phase = "First Quarter"
        elif current_moon_phase_value == 0.5:
            current_moon_phase = "Full Moon"
        elif current_moon_phase_value == 0.75:
            current_moon_phase = "Last Quarter"
        elif 0 < current_moon_phase_value < 0.25:
            current_moon_phase = "Waxing Crescent"
        elif 0.25 < current_moon_phase_value < 0.5:
            current_moon_phase = "Waxing Gibbous"
        elif 0.5 < current_moon_phase_value < 0.75:
            current_moon_phase = "Waning Gibbous"
        else:
            current_moon_phase = "Waning Crescent"

        # Retrieve the icon code based on the moon phase
        moon_icon_name, moon_icon_code = moon_phase_mappings.get(current_moon_phase, ("wi-moon-unknown", "f000"))


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
            'current_weather_summary': current_weather_summary,
            'current_weather_icon': current_weather_icon_code,
            'current_temperature': round(weather_data_2["current"]["temp"]),
            'visibility_distance': round(weather_data_2["current"]["visibility"]//1609),
            'wind_speed': round(weather_data_2["current"]["wind_speed"]),
            'wind_gust': round(weather_data_2["daily"][0]["wind_gust"]),
            'feels_like': round(weather_data_2["current"]["feels_like"]),
            'humidity': round(weather_data_2["current"]["humidity"]),
            'dew_point': round(weather_data_2["current"]["dew_point"]),
            'uv_index': uv_index,
            'uv_index_meaning': uv_index_meaning,
            'air_pressure': air_pressure,
            'todays_avg_air_pressure': todays_avg_air_pressure,
            'current_chance_of_rain': round(weather_data_2["hourly"][0]["pop"]*100),
            # 'daily_chance_of_rain': round(weather_data_2["daily"][0]["pop"]*100),
            'next_hour_chance_of_rain': round(weather_data_2["hourly"][1]["pop"]*100),
            'todays_moonrise_time': todays_moonrise_time,
            'current_moon_phase': current_moon_phase,
            'moon_icon_name': moon_icon_name,
            'moon_icon_code': moon_icon_code,
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
            'daily_forecast_content_list': daily_forecast_content_list,

            'hours': hours,
            'hourly_temps': hourly_temps,
            # 'hourly_rainfall': hourly_rainfall,
            'hourly_weather_icons': hourly_icon_codes,
            'hourly_forecast_content': hourly_forecast_content,
            'hourly_forecast_content_list': hourly_forecast_content_list,
            'hourly_wind_speeds': hourly_wind_speeds,
            'hourly_humidity': hourly_humidity,
            'hourly_air_pressures': hourly_air_pressures,

            'alert_description': alert_description,
            # 'air_quality_index': air_quality_index,
            'aqi_values': aqi_values,
        }

def index(request):
    return render(request, 'form.html')

def stackedareachart(request):
    """
    View for stacked area chart using D3.js.
    """
    nb_element = 100
    xdata = list(range(nb_element))
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = [x * 2 for x in ydata]

    # Prepare chart data
    chartdata = {
        'x': xdata,
        'y1': ydata,
        'y2': ydata2
    }

    context = {
        'chartdata': chartdata
    }
    
    return render(request, 'stackedareachart.html', context)


from .chart_functions import create_chart 

def chart_view(request):
    plot_div = create_chart()
    return render(request, '../templates/components/charts.html', {'plot_div': plot_div})
