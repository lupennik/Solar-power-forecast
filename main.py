import re
import urllib.request
from apixu.client import ApixuClient, ApixuException
# more info about requests: https://www.apixu.com/doc/request.aspx,
# more info about api: ./apixu/client.py or https://github.com/apixu/apixu-python
# azimuth and altitude angles data source: http://aa.usno.navy.mil/data/docs/AltAz.php

api_key = '124b5f7f100647aca80135859172911' #my personal API-key
client = ApixuClient(api_key)

#input provision
print("Program will ask you about your PV and compute power loads in chosen day and hour.")
max_load = input("Maximum PV-system load in Watts: ")
panel_azimuth = input("Panel's azimuth angle in [deg]: ") #TODO: use for computation
tilt = input("Panel's tilt angle in [deg]: ")
dt = input("Forecast day in 'yyyy-mm-dd' format, (1-10 day range): ")
hour = input("Forecast hour (1-24): ")
q = input("City name (in english): ")

#get sun azimuth and altitude angles 
# (now it's for Prague)
url = 'http://aa.usno.navy.mil/cgi-bin/aa_altazw.pl?form=2&body=10' \
      '&year=' + dt[:4] + '&month=' + dt[5:7] + '&day=' + dt[8:10] + '&intv_mag=60&place=Prague&lon_sign=1&lon_deg=' \
      '14&lon_min=25&lat_sign=1&lat_deg=50&lat_min=5&tz=1&tz_sign=-1'
data = urllib.request.urlopen(url).read()
decoded_data = data.decode('utf-8')
#TODO: search for angles in request
""""
m = re.search('<span class="phrase">', decoded_data)
new_str = decoded_data[m.end():m.end()+300]
m = re.search('</span>', new_str)
new_str = new_str[:m.start()]
"""

"""Parameters of getForecastWeather: q='location', dt='yyyy-mm-dd' - forecast date restriction, 'hour' - forecast hour restriction.
Response is in dictionary format."""
requested_forecast = client.getForecastWeather(q=q, dt=dt, hour=hour)
#print(requested_forecast)
print(requested_forecast['location']['country']) # name of country

#TODO: sun_elevation_angle, sun_azimuth_angle from API
#TODO: tilt_loss_koef = math.cos(abs(90-sun_elevation_angle-tilt)) - http://www.reuk.co.uk/wordpress/solar/solar-panel-mounting-angle/

sun_raise = float(requested_forecast['forecast']['forecastday'][0]['astro']['sunrise'][0:2])
sun_set = 12 + float(requested_forecast['forecast']['forecastday'][0]['astro']['sunset'][0:2])

def parabolise_day(time):
    return -((time - sun_set)*(time - sun_raise))

day_position_coef = parabolise_day(int(hour)) / parabolise_day((sun_raise + sun_set) / 2)
tilt_loss_coef =  1 - ((68.5 - float(tilt))/68.5) #68.5 constant is taken from http://www.solarpaneltilt.com for winter angle, 50 deg.
clouds_coef = 1 - requested_forecast['forecast']['forecastday'][0]['hour'][0]['cloud'] / 100
effic_coef = day_position_coef * tilt_loss_coef * clouds_coef

print(effic_coef * int(max_load))
