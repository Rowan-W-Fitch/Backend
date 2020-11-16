from bs4 import BeautifulSoup
import re
import requests
import numpy as np
from rest_framework.response import Response
import json
from apis.serializers import BeachSerializer
from apis.models import Beach

dirs = ['N', 'E', 'S', 'W']

def get_swells(soup):
    swells = soup.find_all('div', {'class':'quiver-swell-measurements'})
    return swells

def clean_swells(swells):
    clean_swells = []
    for swell in swells:
        clean_swells.append(swell.get_text())
    return clean_swells

def get_swell_height(swell):
    return swell.split(' ')[0].split('FT')[0]

def get_swell_period(swell):
    return swell.split(' ')[2].split('s')[0]

def get_swell_dir(swell):
    dir_str =  swell.split(' ')[3][0]
    for i in range(len(dirs)):
        if dir_str == dirs[i]:
            return i
    return 0

def get_wind(soup):
    wind = soup.find('div', {'class': 'quiver-spot-forecast-summary__stat-container quiver-spot-forecast-summary__stat-container--wind'})
    return re.sub(r'Wind', '', re.sub(r'KTS', " ", wind.get_text()))

def get_wind_dir(wind):
    wind_str = wind.split(" ")[1][0]
    for i in range(len(dirs)):
        if wind_str == dirs[i]:
            return i
    return 0

def get_wind_speed(wind):
    return wind.split(" ")[0]


def get_tide(soup):
    tide = soup.find('div', {'class':'quiver-spot-forecast-summary__stat-container quiver-spot-forecast-summary__stat-container--tide'})
    return re.sub(r'Tide','', tide.get_text()).split('FT')[0]


def get_water_temp(soup):
    temp = soup.find('div', {'class': 'quiver-water-temp'})
    return re.sub(r'Water Temp', '', temp.get_text()).split(' - ')[0]


def height_period_dir_dict(clean_swlls):
    height_period_dir_dict = {}
    for swell in clean_swlls:
        height_period_dir_dict[float(get_swell_height(swell))] = [int(get_swell_period(swell)), get_swell_dir(swell)]
    return height_period_dir_dict


def get_longest_period_swell(dict):
    longest = 0
    ans = [-1,-1,-1]
    for key in dict.keys():
        if dict[key][0] > longest:
            ans[0] = key
            ans[1] = dict[key][0]
            ans[2] = dict[key][1]
            longest = dict[key][0]
    return ans


def get_tallest_height(dict):
    tallest = 0
    ans = [-1, -1, -1]
    for key in dict.keys():
        if key > tallest:
            ans[0] = key
            ans[1] = dict[key][0]
            ans[2] = dict[key][1]
            tallest = key
    return ans


def get_data_to_numpy(beach_dir, driving_dist, url, lat, lng):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml') #lxml is a pareser library for structured data
    #wind data
    wind = get_wind(soup)
    wind_speed = get_wind_speed(wind)
    wind_dir = get_wind_dir(wind)
    #swell data
    swells = get_swells(soup)
    clean_swlls = clean_swells(swells)
    #get swell data
    dict = height_period_dir_dict(clean_swlls)
    swell1 = get_longest_period_swell(dict)
    swell1_ht, swell1_pd, swell1_dir = swell1[0], swell1[1], swell1[2]
    swell2 = get_tallest_height(dict)
    swell2_ht, swell2_pd, swell2_dir = swell2[0], swell2[1], swell2[2]
    #tide data
    tide = get_tide(soup)
    #water_temp_data
    temp = get_water_temp(soup)
    return np.array([beach_dir, wind_speed, wind_dir, swell1_ht, swell2_ht, swell1_pd, swell2_pd, swell1_dir, swell2_dir, tide, temp, driving_dist])

def create_beach_api(name, url, beach_dir, lat, lng):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml') #lxml is a pareser library for structured data
    #wind data
    wind = get_wind(soup)
    wind_speed = get_wind_speed(wind)
    wind_dir = get_wind_dir(wind)
    #swell data
    swells = get_swells(soup)
    clean_swlls = clean_swells(swells)
    #get swell data
    dict = height_period_dir_dict(clean_swlls)
    swell1 = get_longest_period_swell(dict)
    swell1_ht, swell1_pd, swell1_dir = swell1[0], swell1[1], swell1[2]
    swell2 = get_tallest_height(dict)
    swell2_ht, swell2_pd, swell2_dir = swell2[0], swell2[1], swell2[2]
    #tide data
    tide = get_tide(soup)
    #water_temp_data
    temp = get_water_temp(soup)
    data = {
        'name': name,
        'surfline_url': url,
        'latitude': lat,
        'longitude': lng,
        'beach_dir': beach_dir,
        'wind_speed': int(wind_speed),
        'wind_dir': wind_dir,
        'swell1_height': swell1_ht,
        'swell2_height': swell2_ht,
        'swell1_period': swell1_pd,
        'swell2_period': swell2_pd,
        'swell1_dir': swell1_dir,
        'swell2_dir': swell2_dir,
        'tide_height': float(tide),
        'water_temp': float(temp)
    }
    #send req to the create beach api endpt
    create_res = requests.post('https://optimal-stoke.herokuapp.com/create_beach', json = data)
    return Response(create_res)

# def update_beach_api(beach_id, url, name, lat, lng, beach_dir):
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'lxml') #lxml is a pareser library for structured data
#     #wind data
#     wind = get_wind(soup)
#     wind_speed = get_wind_speed(wind)
#     wind_dir = get_wind_dir(wind)
#     #swell data
#     swells = get_swells(soup)
#     clean_swlls = clean_swells(swells)
#     #get swell data
#     dict = height_period_dir_dict(clean_swlls)
#     swell1 = get_longest_period_swell(dict)
#     swell1_ht, swell1_pd, swell1_dir = swell1[0], swell1[1], swell1[2]
#     swell2 = get_tallest_height(dict)
#     swell2_ht, swell2_pd, swell2_dir = swell2[0], swell2[1], swell2[2]
#     #tide data
#     tide = get_tide(soup)
#     #water_temp_data
#     temp = get_water_temp(soup)
#     data = {
#         'name': name,
#         'surfline_url': url,
#         'latitude': float(lat),
#         'longitude': float(lng),
#         'beach_dir': beach_dir,
#         'wind_speed': wind_speed,
#         'wind_dir': wind_dir,
#         'swell1_height': float(swell1_ht),
#         'swell2_height': float(swell2_ht),
#         'swell1_period': swell1_pd,
#         'swell2_period': swell2_pd,
#         'swell1_dir': swell1_dir,
#         'swell2_dir': swell2_dir,
#         'tide_height': float(tide),
#         'water_temp': int(temp)
#     }
#     try:
#         beach = Beach.objects.get(id = beach_id)
#     except Beach.DoesNotExist:
#         return False
#
#     serializer = BeachSerializer(beach, data = data)
#     if serializer.is_valid():
#         serializer.save()
#         return True
#     else:
#         return False
