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
dt = '2018-02-09'
hour = 17
q = 'Prague'
lon = 14
lon_min = 25
lat = 50
lat_min = 5
longitude = 14.25
latitude =  50.5
offset = 0

# Clouds
#https://github.com/bitpixdigital/forecastiopy3
key = '9ab53f67e08c8504464553314d509d92'
Prague = [latitude, longitude]
fio = ForecastIO.ForecastIO(key, latitude=Prague[0], longitude=Prague[1])

clouds = []
hourly = FIOHourly.FIOHourly(fio)
print('Filling array of clouds...')
for hour in range(0, hourly.hours()):
    clouds.append(hourly.get_hour(hour)['cloudCover'])

clouds = [0.46, 0.46, 0.46, 0.46, 0.46, 0.46, 0.46, 0.46, 0.46, 0.46]
print(clouds)



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
print(new_str)

sun_elevations = []
sun_azimuths = []
panel_angle_loss_koef = []

#TODO: hours range fix
sml_str = new_str[0].split(':')
hour_st = int(sml_str[0])

for i in range(0, len(new_str), 3):
      sml_str = new_str[i].split(':')
      sun_elevations.append(float(new_str[i + 1]))
      sun_azimuths.append(float(new_str[i + 2]))
      panel_angle_loss_koef.append(sin(radians(tilt)) * cos(radians(float(new_str[i + 1]))) * cos(
            radians(panel_azimuth) - radians(float(new_str[i + 2]))) + cos(radians(tilt)) * sin(
            radians(float(new_str[i + 1]))))
      hour_en = int(sml_str[0])
#print(sun_elevations)
#print(sun_azimuths)
print(panel_angle_loss_koef)


# The equation from https://www.tudelft.nl/en/eemcs/the-faculty/departments/electrical-sustainable-energy/
# photovoltaic-materials-and-devices/dutch-pv-portal/the-model/sun-position-and-components/

effic_coef = []
for i in range(hour_st, hour_en + 1):
    print(clouds[i - hour_st - 1 + offset])
    effic_coef.append(panel_angle_loss_koef[i - hour_st] * (1 - clouds[i - hour_st - 1 + offset]))
    print(str(i) + ': ' + str(panel_angle_loss_koef[i - hour_st] * (1 - clouds[i - hour_st - 1 + offset]) * int(max_load)))

print("Efficience coeficients array: " + str(effic_coef))

for i in range(0, len(effic_coef)):
    effic_coef[i] = effic_coef[i] * int(max_load)
print(effic_coef)

