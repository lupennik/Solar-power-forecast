import scipy as sp
import pickle
import matplotlib.pyplot as plt
import random
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from scipy.stats import pearsonr
from sklearn import preprocessing


def svm_run():
    data = read_data(False)
    DRAW_N = 50

    training_features, testing_features, training_labels, testing_labels = train_test_split(data[:, :-1], data[:, -1], test_size=0.4)

    clf = SVR(kernel='rbf', C=2, gamma=0.5)
    clf.fit(training_features, training_labels)
    y_rbf = clf.predict(testing_features)

    # validation of the model
    # print(clf.score(testing_features, testing_labels))
    scores = cross_val_score(clf, data[:, :-1], data[:, -1], cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    if DRAW_N < testing_labels.shape[0]:
        fig, ax = plt.subplots()
        ax.plot(sp.arange(DRAW_N), testing_labels[:DRAW_N], color='g', lw=2, label='Real data')
        ax.plot(sp.arange(DRAW_N), y_rbf[:DRAW_N], color='navy', lw=2, label='RBF model')
        plt.legend(loc='upper right')
        fig.savefig("graphs/SVR_vol.01_" + str(random.randint(0, 10000)) + ".png")
        plt.show()
    else:
        print("too high DRAW_N")


# sun_rad / power plot + another subgraph with testing data
# heat map (temp, sun_irrad) => power
def visualise_data():
    # xx, yy = sp.meshgrid(sp.linspace(-4, 4, 100),
    #                      sp.linspace(-4, 4, 100))
    # X = sp.array([data[r_test_idx[:TEST_SAMPLES_N], -1], data[r_test_idx[:TEST_SAMPLES_N], 4]])
    # X = sp.transpose(X)
    # clf = EllipticEnvelope(contamination=0.05)
    # y_pred = clf.fit(X).predict(X)
    # Z = clf.predict(sp.c_[xx.ravel(), yy.ravel()])
    # Z = Z.reshape(xx.shape)
    # plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='black')
    #
    # colors = sp.array(['#377eb8', '#ff7f00'])
    # plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[(y_pred + 1) // 2])

    # print(pearsonr(data[r_test_idx[:TEST_SAMPLES_N], 5], data[r_test_idx[:TEST_SAMPLES_N], 6]))
    # print(pearsonr(data[r_test_idx[:TEST_SAMPLES_N], 5], data[r_test_idx[:TEST_SAMPLES_N], 8]))
    # plt.scatter(data[r_test_idx[:TEST_SAMPLES_N], 5], data[r_test_idx[:TEST_SAMPLES_N], 6])
    plt.savefig("graphs/pic" + str(random.randint(0, 10000)) + ".png")
    plt.show()

def preproces(data, slopes_needed):
    training_data = data
    training_data = sp.array(training_data[:, slopes_needed])

    # overliers reducing with std dev
    mean = sp.mean(training_data, axis=0)
    sd = sp.std(training_data, axis=0)

    for i in range(training_data.shape[1]):
        training_data = training_data[training_data[:, i] < mean[i] + 2 * sd[i]]
        training_data = training_data[training_data[:, i] > mean[i] - 2 * sd[i]]

    # specific features manipulation ! SUN DAY DURATION AT DATA[4] AND POWER INFO AT DATA[-1] !
    training_data = training_data[training_data[:, -1] > 20]
    training_data = training_data[training_data[:, -1] < 650]
    # training_data = training_data[training_data[:, 4] > 8]
    # training_data = training_data[training_data[:, 4] < 16.5]

    sp.random.shuffle(training_data)
    return training_data

filenames = ['Air_moisture_perc.csv', 'Humidity_mm.csv', 'Pressure_mean_hpa.csv',
            'Snow_h_cm.csv', 'Sun_irrad_hours.csv', 'Temp_max.csv', 'Temp_min.csv',
            'Wind_mean.csv', 'Temp_mean.csv']

def read_data(is_in_data_file):

    # if true, file data read
    if (is_in_data_file):
        with open('data/data', 'rb') as f:
            data = pickle.load(f)
            return data

    power_data = sp.delete(sp.genfromtxt("data/Power_history.csv", delimiter=","), 0, 1).flatten()

    weather_data = sp.stack([x.flatten() for x in sp.delete([sp.genfromtxt("data/" + filename, delimiter=",") for filename in filenames], [0, 1], 2)])
    weather_data = sp.delete(weather_data, sp.s_[:18], 1)

    # preprocessing
    # reduce missing data
    weather_data = sp.stack(x[~sp.isnan(x)] for x in weather_data)
    weather_data = sp.stack(x[~sp.isnan(power_data)] for x in weather_data)
    power_data = power_data[~sp.isnan(power_data)]
    data = sp.vstack([weather_data, power_data])
    data = data.transpose()
    data = preproces(data, [4, -1])

    # writing output data to file data
    # with open('data/data', 'wb') as f:
    #     pickle.dump(data, f)
    return data

svm_run()