import re
from urllib.request import *
import json
import datetime

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

# inserted explicitly
parameters = ["fog", "hail", "heatingdegreedays", "humidity", "maxdewpti", "maxdewptm", "maxhumidity",
              "maxpressurei",
              "maxpressurem", "maxtempi", "maxtempm", "maxvisi", "maxvism", "maxwspdi", "maxwspdm", "meandewpti",
              "meandewptm", "meanpressurei", "meanpressurem", "meantempi", "meantempm", "meanvisi", "meanvism",
              "meanwdird",
              "meanwindspdi", "meanwindspdm", "mindewpti", "mindewptm", "minhumidity", "minpressurei",
              "minpressurem",
              "mintempi", "mintempm", "minvisi", "minvism", "minwspdi", "minwspdm", "rain", "snow"]

#writes history weather using API from forecast date to (forecast date - n_days)
def write_w_history_to_file(forecast_date, n_days, API_key, country_shortcut, city_name, params):
    date = datetime.datetime(int(forecast_date[:4]), int(forecast_date[5:7]), int(forecast_date[8:10]))
    parsed_json = {}
    statistic_data = [[] for i in range(n_days)]

    for i in range(n_days):
        d_iso = date.isoformat()
        f = urlopen('http://api.wunderground.com/api/' + API_key + '/' + 'history_' + d_iso[:4] + d_iso[5:7] + d_iso[8:10] + '/q' + '/' + country_shortcut + '/' + city_name + '.json')
        json_string = f.read()
        f.close()
        parsed_json[d_iso[:10]] = json.loads(json_string)

        with open("history", 'w') as fw:
            fw.write(json.dumps(parsed_json, indent=4, sort_keys=True))

        for item in params:
            statistic_data[i].append(parsed_json[d_iso[:10]]["history"]["dailysummary"][0][item])

        date -= datetime.timedelta(days=1)

    return statistic_data

def read_w_history_from_file(forecast_date, n_days, params):
    f_d = forecast_date
    fr = open("history", 'r')
    json_string = fr.read()
    fr.close()
    parsed_json = json.loads(json_string)

    statistic_data = [[] for i in range(n_days)]

    for i in range(n_days):
        for item in params:
            statistic_data[i].append(parsed_json[f_d]["history"]["dailysummary"][0][item])

        f_d = f_d[:8] +  str(int(f_d[8:10]) - 1)

    return statistic_data