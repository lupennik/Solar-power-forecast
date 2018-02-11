import json
from data_receiver import *
from calculation_func import *


wanna_graf = True

#panel configuration
max_load = 5 #kWp
panel_azimuth = 180
panel_tilt = 65

#forecast time
forecast_date = '2018-02-13'
forecast_hour = '10'

#forecast coordinates (50°06'10.7"N 14°23'30.3"E - FEL ČVUT)
city_name = 'Prague'
country_shortcut = 'CZ'
API_key = 'f70b0eafc160a74b'
lon = 14
lon_min = 23
lat = 50
lat_min = 6
longitude = 14.23
latitude =  50.6

#input
very_big_weather_list = write_weather_to_file(API_key, country_shortcut, city_name)
angles = write_sun_angles_to_file(forecast_date, city_name, lat, lat_min, lon, lon_min).split()
astronomy = read_astronomic_from_file()

#find_forecast_for_hour(very_big_weather_list, angles, astronomy, forecast_hour, forecast_date, panel_tilt, panel_azimuth, max_load)

find_forecast_for_day(very_big_weather_list, angles, astronomy, forecast_date, panel_tilt, panel_azimuth, max_load, wanna_graf)



"""
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
      panel_angle_loss_koef.append(sin(radians(panel_tilt)) * cos(radians(float(new_str[i + 1]))) * cos(
            radians(panel_azimuth) - radians(float(new_str[i + 2]))) + cos(radians(panel_tilt)) * sin(
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
"""