import scipy as sp
import pickle
import matplotlib.pyplot as plt
import random
from sklearn.svm import SVR
from sklearn import preprocessing

def svm_run():
    training_data = read_data(True)

    #we take last 50 values for tests and rest for training SVM
    training_features = preprocessing.robust_scale(training_data[:-50, :])
    training_labels = training_data[:-50, 8]
    testing_features = preprocessing.robust_scale(training_data[-50:, :])
    testing_labels = training_data[-50:, 8]

    svr_rbf = SVR(kernel='rbf')
    svr_rbf.fit(training_features, training_labels)
    y_rbf = svr_rbf.predict(testing_features)

    fig, ax = plt.subplots()
    ax.plot(sp.arange(50), testing_labels, color='g', lw=2, label='Real data')
    ax.plot(sp.arange(50), y_rbf, color='navy', lw=2, label='RBF model')
    fig.savefig("graphs/SVR_vol.01.png")
    plt.show()


def visualise_data(data):
    fig, ax = plt.subplots()
    x = sp.arange(data[8].shape[0])
    ax.plot(x, data[8])

    fig.savefig("graphs/pic" + str(random.randint(0, 10000))  + ".png")


def read_data(is_in_data_file):

    if (is_in_data_file):
        with open('data/data', 'rb') as f:
            training_data = pickle.load(f)
            return training_data

    filenames = ['Air_moisture_perc.csv', 'Humidity_mm.csv', 'Pressure_mean_hpa.csv',
                 'Snow_h_cm.csv', 'Sun_irrad_hours.csv', 'Temp_max.csv', 'Temp_min.csv',
                 'Wind_mean.csv']

    power_data = sp.delete(sp.genfromtxt("data/Power_history.csv", delimiter=","), 0, 1).flatten()

    weather_data = sp.stack([x.flatten() for x in sp.delete([sp.genfromtxt("data/" + filename, delimiter=",") for filename in filenames], [0, 1], 2)])
    weather_data = sp.delete(weather_data, sp.s_[:18], 1)

    # preprocessing
    #reduce missing data
    weather_data = sp.stack(x[~sp.isnan(x)] for x in weather_data)
    weather_data = sp.stack(x[~sp.isnan(power_data)] for x in weather_data)
    power_data = power_data[~sp.isnan(power_data)]

    #stack weather and power data together
    training_data = sp.vstack([weather_data, power_data])

    #reduce values values that overlay power interval (20, 650)
    training_data = sp.array([training_data[x][~(training_data[8] < 20)] for x in range(training_data.shape[0])])
    training_data = sp.array([training_data[x][~(training_data[8] > 650)] for x in range(training_data.shape[0])])
    training_data = training_data.transpose()

    with open('data/data', 'wb') as f:
        pickle.dump(training_data, f)

    return training_data

svm_run()