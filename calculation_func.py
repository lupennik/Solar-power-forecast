from math import *
import matplotlib.pyplot as plt
import numpy as np

def find_forecast_for_day(very_big_weather_list, angles, astronomy, forecast_date, panel_tilt, panel_azimuth, max_load, wanna_graf):
    start = int(astronomy['sun_phase']['sunrise']['hour']) + 1
    end = int(astronomy['sun_phase']['sunset']['hour']) + 1

    # looking for requested hour (clouds)
    clouds = []
    for i in range(len(very_big_weather_list["hourly_forecast"])):
        if (very_big_weather_list["hourly_forecast"][i]['FCTTIME']['mday_padded'] == forecast_date[8:10]):
            for i2 in range(i + start, i + end):
                #print(str(very_big_weather_list["hourly_forecast"][i2]['FCTTIME']['pretty']) + ': ' +str(very_big_weather_list["hourly_forecast"][i2]['sky']))
                clouds.append(int(very_big_weather_list["hourly_forecast"][i2]['sky']))
            break;

    # looking for requested hour (angles)
    sun_elevations = []
    sun_azimuths = []
    for i in range(0, len(angles), 3):
        sml_str = angles[i].split(':')
        if (int(sml_str[0]) == start):
            for i2 in range(i, 3 *(i + end - start - 2), 3):
                sun_elevations.append(float(angles[i2 + 1]))
                sun_azimuths.append(float(angles[i2 + 2]))
            break

    kws = []
    for i in range(0, end - start):
        kws.append((1 - float(clouds[i]) / 100) * (sin(radians(panel_tilt)) * cos(radians(float(sun_elevations[i]))) * cos(
        radians(panel_azimuth) - radians(float(sun_azimuths[i]))) + cos(radians(panel_tilt)) * sin(
        radians(float(sun_elevations[i])))) * max_load)


    if (wanna_graf == True):
        t = np.arange(start, end, 1)
        fig, ax = plt.subplots()
        ax.plot(t, kws, 'ro', label = "My model")
        ax.plot(t, [0.9, 1.8, 2.6, 2.9, 2.2, 0.8, 0.8, 0.8, 0.6, 0.2], 'g--', label = "Forkast") #ax.plot(t, [compared graf], 'g')
        ax.set(xlabel='time (hours)', ylabel='power (kW)',
               title='Power forecast for ' + forecast_date)
        ax.legend()
        ax.grid()
        plt.xlim(7, 18)
        plt.ylim(0, 5)
        fig.savefig("forecast_angle" + forecast_date + ".png")
        plt.show()

    print(kws)

    return kws


def find_forecast_for_hour(very_big_weather_list, angles, astronomy, forecast_hour, forecast_date, panel_tilt, panel_azimuth, max_load):

    if (int(astronomy['sun_phase']['sunrise']['hour']) >= int(forecast_hour)):
        return 0
    elif (int(astronomy['sun_phase']['sunset']['hour']) < int(forecast_hour)):
        return 0


    # looking for requested hour (clouds)
    cloud = 0
    for i in range(len(very_big_weather_list["hourly_forecast"])):
        if (very_big_weather_list["hourly_forecast"][i]['FCTTIME']['hour_padded'] == forecast_hour):
            if (very_big_weather_list["hourly_forecast"][i]['FCTTIME']['mday_padded'] == forecast_date[8:10]):
                cloud = very_big_weather_list["hourly_forecast"][i]['sky']
                break;

    # looking for requested hour (angles)
    sun_elevation = 0
    sun_azimuth = 0
    for i in range(0, len(angles), 3):
        sml_str = angles[i].split(':')
        if (sml_str[0] == forecast_hour):
            sun_elevation = float(angles[i + 1])
            sun_azimuth = float(angles[i + 2])
            break;

    # Equation from https://www.tudelft.nl/en/eemcs/the-faculty/departments/electrical-sustainable-energy/
    # photovoltaic-materials-and-devices/dutch-pv-portal/the-model/sun-position-and-components/
    panel_angle_loss_coef = sin(radians(panel_tilt)) * cos(radians(float(sun_elevation))) * cos(
        radians(panel_azimuth) - radians(float(sun_azimuth))) + cos(radians(panel_tilt)) * sin(
        radians(float(sun_elevation)))

    effic_coef = panel_angle_loss_coef * (1 - float(cloud) / 100)

    # Arguable miltiplication
    final_load = effic_coef * max_load

    print(final_load)

    return final_load