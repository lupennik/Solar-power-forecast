from sklearn.svm import SVR
import matplotlib.pyplot as plt
from data_receiver import *

with open('api_key', 'r') as fr:
    API_key = fr.read()

city_name = 'Prague'
country_shortcut = 'CZ'
forecast_date = '2018-02-14'


# Generate sample data
write_data_for_wh_and_ph()
X = read_noaa_w_history()
y = read_power_history()

print('hey')
# X = write_w_history_to_file(forecast_date, 5, API_key, country_shortcut, city_name) #writes days to file weather_history and returns array of
#                                                                                      #samples descending (from forecast_date to forecast_date - n_days)
# X = read_w_history_from_file(forecast_date[:8] + str(int(forecast_date[8:]) - 1), 5)  #reads days from file and retyrn array of samples descending
# Read real power load data
# y = [11.95, 8.75, 2.875, 3.275, 7.9] #09, 10, 11, 12, 13...  17.825 - 14.02.
# #############################################################################
# Fit regression model
# forecast_day_weather = read_w_history_from_file(forecast_date, 1)


# svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
# svr_lin = SVR(kernel='linear', C=1e3)
# svr_poly = SVR(kernel='poly', C=1e3, degree=2)
# y_rbf = svr_rbf.fit(X, y)
# y_lin = svr_lin.fit(X, y)
# y_poly = svr_poly.fit(X, y)
#
# # X.append(forecast_day_weather[0])
# # y.append(17.825)
#
# y_rbf = svr_rbf.predict(X)
# y_lin = svr_lin.predict(X)
# y_poly = svr_poly.predict(X)
#
# # #############################################################################
# # Look at the results
# x = [1, 2, 3, 4, 5, 6]
# lw = 2
# fig, ax = plt.subplots()
# ax.plot(x, y, color='g', lw=lw, label='Real data')
# ax.plot(x, y_rbf, color='navy', lw=lw, label='RBF model')
# ax.plot(x, y_lin, color='c', lw=lw, label='Linear model')
# ax.plot(x, y_poly, color='cornflowerblue', lw=lw, label='Polynomial model')
# ax.set(xlabel = 'data', ylabel = 'target', title = 'Support Vector Regression for: ' + forecast_date)
# plt.legend()
# fig.savefig("SVR_" + forecast_date + ".png")
# plt.show()