import re
from urllib.request import *
import json

def read_weather_from_file():
    fr = open("weather", 'r')
    json_string = fr.read()
    fr.close()
    parsed_json = json.loads(json_string)
    return parsed_json

def read_astronomic_from_file():
    fr = open("astronomy", 'r')
    json_string = fr.read()
    fr.close()
    parsed_json = json.loads(json_string)
    return parsed_json

def write_weather_to_file(API_key, country_shortcut, city_name):
    f = urlopen('http://api.wunderground.com/api/' + API_key + '/hourly10day/q/' + country_shortcut + '/' + city_name + '.json')
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    fw = open("weather", 'w')
    fw.write(json.dumps(parsed_json, indent=4, sort_keys=True))
    fw.close()

    f = urlopen('http://api.wunderground.com/api/' + API_key + '/astronomy/q/' + country_shortcut + '/' + city_name + '.json')
    json_string = f.read()
    f.close()
    parsed = json.loads(json_string)
    fw = open("astronomy", 'w')
    fw.write(json.dumps(parsed, indent=4, sort_keys=True))
    fw.close()

    return parsed_json



def write_sun_angles_to_file(forecast_date, city_name, lat, lat_min, lon, lon_min):
    url = 'http://aa.usno.navy.mil/cgi-bin/aa_altazw.pl?form=2&body=10' \
          '&year=' + forecast_date[:4] + '&month=' + forecast_date[5:7] + '&day=' + forecast_date[
                                                              8:10] + '&intv_mag=60&place=' + city_name + '&lon_sign=1&lon_deg=' \
          + str(lon) + '&lon_min=' + str(lon_min) + '&lat_sign=1&lat_deg=' + str(lat) + '&lat_min=' + str(
        lat_min) + '&tz=1&tz_sign=1'
    data = urlopen(url).read()
    decoded_data = data.decode('utf-8')
    #print(url)

    # TODO: bad search, make better
    m = re.search('h  m', decoded_data)
    texted_angles = decoded_data[m.end() + 232:m.end() + 550]
    fp = open('angles', 'w')
    fp.write(texted_angles)
    fp.close()
    return texted_angles