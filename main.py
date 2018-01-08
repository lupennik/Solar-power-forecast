import re
from math import *
from forecastiopy import *
import urllib.request
import matplotlib
#apixu-api usage
"""from apixu.client import ApixuClient, ApixuException
more info about requests: https://www.apixu.com/doc/request.aspx,
more info about api: ./apixu/client.py or https://github.com/apixu/apixu-python
api_key = '124b5f7f100647aca80135859172911' #my personal API-key
client = ApixuClient(api_key)
Parameters of getForecastWeather: q='location', dt='yyyy-mm-dd' - forecast date restriction, 'hour' - forecast hour restriction.
Response is a dictionary.
requested_forecast = client.getForecastWeather(q=q, dt=dt)
print(requested_forecast)
print(requested_forecast['location']['country']) # name of country
"""

#input
max_load = 5 #kWp
panel_azimuth = 180
tilt = 65
dt = '2018-01-04'
hour = 17
q = 'Prague'
lon = 14
lon_min = 25
lat = 50
lat_min = 5
longitude = 14.25
latitude =  50.5

# Clouds
#https://github.com/bitpixdigital/forecastiopy3
key = '9ab53f67e08c8504464553314d509d92'
Prague = [latitude, longitude]
fio = ForecastIO.ForecastIO(key, latitude=Prague[0], longitude=Prague[1])

clouds = []
hourly = FIOHourly.FIOHourly(fio)
print('Filling array of clouds...')
for hour in range(0, hourly.hours()):
    print('Hour', hour+1)
    clouds.append(hourly.get_hour(hour)['cloudCover'])
#print(clouds)

# Angles
# Sun azimuth and altitude angles data source: http://aa.usno.navy.mil/data/docs/AltAz.php
# get sun azimuth and altitude angles
# params: date, place name (opt.), longitude, longitude_minutes, lattitude, lattitude_minutes
url = 'http://aa.usno.navy.mil/cgi-bin/aa_altazw.pl?form=2&body=10' \
      '&year=' + dt[:4] + '&month=' + dt[5:7] + '&day=' + dt[8:10] + '&intv_mag=60&place=' + q + '&lon_sign=1&lon_deg=' \
      + str(lon) + '&lon_min=' + str(lon_min) + '&lat_sign=1&lat_deg=' + str(lat) + '&lat_min=' + str(lat_min) + '&tz=1&tz_sign=1'
data = urllib.request.urlopen(url).read()
decoded_data = data.decode('utf-8')
print(url)
#TODO: bad search, make better
m = re.search('h  m', decoded_data)
new_str = decoded_data[m.end()+232:m.end()+550]
new_str = new_str.split()
#print(new_str)

sun_elevations = []
sun_azimuths = []
#TODO: hours range fix
for i in range(0, len(new_str), 3):
      sml_str = new_str[i].split(':')
      if (int(sml_str[0]) == hour):
            sun_elevations.append(float(new_str[i + 1]))
            sun_azimuths.append(float(new_str[i + 2]))


"""
# The equation from https://www.tudelft.nl/en/eemcs/the-faculty/departments/electrical-sustainable-energy/
# photovoltaic-materials-and-devices/dutch-pv-portal/the-model/sun-position-and-components/
panel_angle_loss_koef = sin(radians(tilt))*cos(radians(sun_elevation))*cos(radians(panel_azimuth)-radians(sun_azimuth))+cos(radians(tilt))*sin(radians(sun_elevation))
print("Percantage of solar irradiation with respect to panel orientation: " + str(panel_angle_loss_koef))

clouds_coef = 0.5
effic_coef = panel_angle_loss_koef * clouds_coef

print(effic_coef * int(max_load))
"""