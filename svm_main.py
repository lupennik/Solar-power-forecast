import numpy as np
import scipy
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from data_receiver import *

city_name = 'Prague'
country_shortcut = 'CZ'
API_key = 'f70b0eafc160a74b'
forecast_date = '2018-02-13'

"""
# Generate sample data
#X = write_w_history_to_file(forecast_date, 5, API_key, country_shortcut, city_name, parameters)
X = read_w_history_from_file(forecast_date, 5, parameters)
# Read real power load data
y = [11.95, 8.75, 2.875, 3.275, 7.9 ] #09, 10, 11, 12, 13...  17.825 - 14.02.
# #############################################################################
# Fit regression model
par, forecast_day_weather = write_w_history_to_file(forecast_date[:8] + str(int(forecast_date[8:]) + 1), 1, API_key, country_shortcut, city_name, parameters)
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y)
y_lin = svr_lin.fit(X, y)
y_poly = svr_poly.fit(X, y)

X.append(forecast_day_weather[0])
y.append(17.825)

y_rbf = svr_rbf.predict(X)
y_lin = svr_lin.predict(X)
y_poly = svr_poly.predict(X)

# #############################################################################
# Look at the results
x = [1, 2, 3, 4, 5, 6]
lw = 2
plt.plot(x, y, color='navy', lw=lw, label='RBF model')
plt.plot(x, y_rbf, color='navy', lw=lw, label='RBF model')
plt.plot(x, y_lin, color='c', lw=lw, label='Linear model')
plt.plot(x, y_poly, color='cornflowerblue', lw=lw, label='Polynomial model')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()
"""