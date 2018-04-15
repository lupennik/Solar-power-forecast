import re
from urllib.request import *
import json
import numpy as np
import datetime

#for WB forecast
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

#for BB forecast SVM vol. 00
# inserted explicitly
parameters = ["fog", "hail", "heatingdegreedays", "humidity", "maxdewpti", "maxdewptm", "maxhumidity",
              "maxpressurei",
              "maxpressurem", "maxtempi", "maxtempm", "maxvisi", "maxvism", "maxwspdi", "maxwspdm", "meandewpti",
              "meandewptm", "meanpressurei", "meanpressurem", "meantempi", "meantempm", "meanvisi", "meanvism",
              "meanwdird",
              "meanwindspdi", "meanwindspdm", "mindewpti", "mindewptm", "minhumidity", "minpressurei",
              "minpressurem",
              "mintempi", "mintempm", "minvisi", "minvism", "minwspdi", "minwspdm", "rain", "snow"]
#communication with file weather_history !!! + API wunderground
def write_w_history_to_file(forecast_date, n_days, API_key, country_shortcut, city_name):
    date = datetime.datetime(int(forecast_date[:4]), int(forecast_date[5:7]), int(forecast_date[8:10]))
    with open("weather_history", 'r') as fr:
        parsed_json = json.loads(fr.read())

    statistic_data = [[] for i in range(n_days)]

    for i in range(n_days):
        d_iso = date.isoformat()
        f = urlopen('http://api.wunderground.com/api/' + API_key + '/' + 'history_' + d_iso[:4] + d_iso[5:7] + d_iso[8:10] + '/q' + '/' + country_shortcut + '/' + city_name + '.json')
        json_string = f.read()
        f.close()

        if (d_iso[:10] not in parsed_json or parsed_json[d_iso[:10]] != json.loads(json_string)):
            parsed_json[d_iso[:10]] = json.loads(json_string)
            with open("weather_history", 'w') as fw:
                fw.write(json.dumps(parsed_json, indent=4, sort_keys=True))

        for item in parameters:
            statistic_data[i].append(parsed_json[d_iso[:10]]["weather_history"]["dailysummary"][0][item])

        date -= datetime.timedelta(days=1)

    return statistic_data
def read_w_history_from_file(forecast_date, n_days):
    date = datetime.datetime(int(forecast_date[:4]), int(forecast_date[5:7]), int(forecast_date[8:]))
    d_iso = date.isoformat()

    fr = open("weather_history", 'r')
    json_string = fr.read()
    fr.close()
    parsed_json = json.loads(json_string)

    statistic_data = [[] for i in range(n_days)]

    for i in range(n_days):
        for item in parameters:
            statistic_data[i].append(parsed_json[d_iso[:10]]["weather_history"]["dailysummary"][0][item])

        date -= datetime.timedelta(days=1)
        d_iso = date.isoformat()


    return statistic_data



# SVM vol. 01
#communicates with weather_history (parses data from graph.csv (PV lab), NOAA history database PRAHA_KARLOV.txt),
#adds info about days missing to file datesofzero and format data
def read_noaa_w_history():
    with open('weather_history', 'r') as fr:
        weather_data = fr.read()
        weather_data = json.loads(weather_data)

        return weather_data
def read_power_history():
    with open('power_history', 'r') as fr:
        power_data = fr.read()
        power_data = json.loads(power_data)

        return power_data
def write_data_for_wh_and_ph():

    with open('PRAHA_KARLOV.txt', 'r') as fr:
        lst_weather = fr.read()
    dates = re.findall('\d{8}', lst_weather)
    lst_weather = lst_weather.split()

    with open('graph.csv', 'r') as fr:
        lst_power = fr.read()
    lst_power = lst_power.split()
    idxs_forbidden = []

    # collect all days with 0 power or not in weather file but in graph file
    for x in range(2, lst_power.__len__(), 3):
        if (float(lst_power[x]) == 0 or not dates.__contains__(
                lst_power[x - 2][6:] + lst_power[x - 2][3:5] + lst_power[x - 2][0:2])):
            idxs_forbidden.append(lst_power[x - 2])
    # collect all days not in graph.csv but in weather history
    for date in dates:
        if (not lst_power.__contains__(date[6:8] + '.' + date[4:6] + '.' + date[0:4])):
            idxs_forbidden.append(date[6:8] + '.' + date[4:6] + '.' + date[0:4])
    dates.clear()

    # writes all unconsisted dates in file datesofzero
    with open('datesofzero', 'w') as fw:
        fw.write(json.dumps(idxs_forbidden))

    # dumps all power history to file power_history without zero powers
    lst_power = np.array(lst_power)
    lst_power = np.reshape(lst_power, (int(lst_power.__len__() / 3), 3))
    lst2 = []
    for i in lst_power:
        if (not idxs_forbidden.__contains__(i[0])):
            lst2.append(i)
    lst2 = np.array(lst2)
    lst_power = lst_power.tolist()
    lst_power.clear()

    lst2 = np.delete(lst2, [0, 1], 1)
    lst2 = lst2.flatten().tolist()
    with open('power_history', 'w') as fw:
        fw.write(json.dumps(lst2))

    # dumps all weather history to file weather_history without zero and missing powers
    dates_forbidden = idxs_forbidden
    lst_weather = np.array(lst_weather)
    lst_weather = np.delete(lst_weather, range(16), 0)
    lst_weather = np.reshape(lst_weather, (int(lst_weather.__len__() / 22), 22))
    lst_weather = np.delete(lst_weather, [0, 1, 4, 6, 8, 10, 12, 14, 19, 20], 1)
    for i in range(lst_weather.__len__()):
        if (not dates_forbidden.__contains__(
                lst_weather[i][0][6:] + '.' + lst_weather[i][0][4:6] + '.' + lst_weather[i][0][:4])):
            lst_power.append(lst_weather[i])
    lst_power = np.delete(lst_power, 0, 1)
    lst_weather = lst_weather.tolist()
    lst_weather.clear()
    for i in range(lst_power.__len__()):
        if (lst_power[i][7] == '999.9'):
            lst_power[i][7] = '0'
        lst_power[i][8] = lst_power[i][8].split('*')[0]
        lst_power[i][9] = lst_power[i][9].split('*')[0]
        lst_power[i][10] = int(lst_power[i][10], 2)
    lst_power = lst_power.tolist()

    with open('weather_history', 'w') as fw:
        fw.write(json.dumps(lst_power))