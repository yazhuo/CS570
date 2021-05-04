from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict
import pickle
import os
import pandas as pd

# The list of datacenters
DC = ["dc_1384",
      "dc_1448",
      "dc_1731",
      "dc_1831",
      "dc_1870",
      "dc_189",
      "dc_1966",
      #   "dc_1980",
      #   "dc_66",
      #   "dc_67",
      #  "dc_85",
      "dc_924"
      #   "lax_1319"
      ]

# feature_path = "/research/yazhuo/ALL_DATA/CDN/features/"
feature_path = './features/'
freq = "/freqnew.p"
size = "/sizenew.p"
burst = "/burst.csv"

# output_path = "/research/yazhuo/ALL_DATA/CDN/clusters/"  # store the cluster result, named as the clustering function
output_path = './clusters/'

feature_selection_path = './selection/'


def getValidIDs(dc):  # read the valid cutomer ids
    validIDs = []
    with open(output_path + dc + "/customerids.txt", "r") as f:
        for id in f.readlines():
            validIDs.append(id.strip())
    return validIDs


def readAttr(dc):  # read the features
    validIDs = getValidIDs(dc)
    attr_dict = defaultdict(list)

    # read burst
    with open(feature_path + dc + burst, 'r') as csv_file:
        csvreader = csv.reader(csv_file)
        fields = next(csvreader)
        for row in csvreader:
            if row[0] in validIDs:  # only keep the valid customers
                for val in row[-11:-1]:  # only keep the last 10 time window
                    attr_dict[row[0]].append(int(val))

    # read and append freqency
    with open(feature_path + dc + freq, 'rb') as pickle_file:
        freq_dict = pickle.load(pickle_file)

        for key, vals in freq_dict.items():
            for val in vals:
                if key in attr_dict.keys():  # only keep the valid customers
                    attr_dict[key].append(val)

    # read and append size
    with open(feature_path + dc + size, 'rb') as pickle_file:
        size_dict = pickle.load(pickle_file)
        for key, vals in size_dict.items():
            for val in vals:
                if key in attr_dict.keys():  # only keep the valid customers
                    attr_dict[key].append(val)

    customer_ids = attr_dict.keys()

    # print(dc, len(validIDs), len(customer_ids))

    return customer_ids, list(attr_dict.values())


def preprocess(X):
    scaler = preprocessing.StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # X_scaled = preprocessing.normalize(X, axis=0)
    return X_scaled


def feature_selection():
    for dc in DC:
        tmp_folder = os.path.exists(feature_selection_path + '/' + dc + '/')
        if not tmp_folder:
            os.makedirs(feature_selection_path + '/' + dc + '/')
        tmp_file = open(feature_selection_path + '/' + dc + '/' + dc + '.csv', 'w')
        writer = csv.writer(tmp_file)
        writer.writerow(['n_clusters', 'feature_list', 'corresponding sse'])
        plt.figure()
        for n_clusters in range(2, 16, 2):
            # print(n_clusters)
            customer_ids, attrs = readAttr(dc)

            X = np.array(attrs)
            X = preprocess(X)
            X = np.transpose(X)

            feature_list = list(range(X.shape[0]))
            sse_list = []
            selected_feature_number = []
            selected_feature = []

            while len(selected_feature_number) < X.shape[0]:
                # print("_______________", selected_feature_number)
                min_sse = float('inf')
                tmp_selected_feature_number = -1
                for tmp_feature in feature_list:
                    # print(tmp_feature)
                    if tmp_feature in selected_feature_number:
                        continue
                    else:
                        selected_feature.append(list(X[tmp_feature]))
                        tmp_X = np.transpose(np.array(selected_feature))
                        # clusterer = KMeans(n_clusters=n_clusters, random_state=0).fit(tmp_X)
                        clusterer = KMedoids(n_clusters=n_clusters, random_state=0, init='k-medoids++').fit(tmp_X)
                        sse = clusterer.inertia_
                        if sse < min_sse:
                            min_sse = sse
                            del selected_feature[-1]
                            tmp_selected_feature_number = tmp_feature
                        else:
                            del selected_feature[-1]
                selected_feature.append(list(X[tmp_selected_feature_number]))
                selected_feature_number.append(tmp_selected_feature_number)
                sse_list.append(min_sse)
            writer.writerow([n_clusters, selected_feature_number, sse_list])
            plt.plot(range(X.shape[0]), sse_list, label="number of clusters: " + str(n_clusters))
        plt.xlabel('added features')
        plt.ylabel('SSE')
        plt.legend()
        plt.savefig(feature_selection_path + '/' + dc + '/' + dc + '_' + str(n_clusters) + '.png')


def cluster_plot(num_feature_list):
    k = 0
    for dc in DC:
        print(dc)
        tmp_file = pd.read_csv(feature_selection_path + '/' + dc + '/' + dc + '.csv')
        n_cluster = tmp_file["n_clusters"]
        SSE_list = tmp_file["corresponding sse"]
        SSE = []
        for l in SSE_list:
            l = list(map(float, l[1:-1].split(', ')))
            SSE.append(l[num_feature_list[k]])
        print(n_cluster)
        # print(SSE)
        plt.figure()
        plt.plot(n_cluster, SSE)
        plt.xlabel("number of clusters")
        plt.ylabel("SSE")
        plt.title("select first " + str(num_feature_list[k]) + " features for each n_clusters")
        plt.savefig(feature_selection_path + '/' + dc + '/' + dc + '_fixed_feature' + '.png')
        k += 1


def cluster(num_cluster_list, num_feature_list):
    k = 0
    for dc in DC:
        n_clusters = num_cluster_list[k]
        n_features = num_feature_list[k]
        print(n_clusters, n_features)
        customer_ids, attrs = readAttr(dc)
        X = np.array(attrs)
        X = preprocess(X)

        tmp_file = pd.read_csv(feature_selection_path + '/' + dc + '/' + dc + '.csv')
        n_feature = tmp_file["feature_list"].tolist()[int(n_clusters/2) - 1]
        n_feature = n_feature[1:-1].split(',')[:n_features]
        n_feature = list(map(int, n_feature))
        print(n_feature)

        X = X[:, n_feature]
        print(X.shape)

        clusterer = KMedoids(n_clusters=n_clusters, random_state=0, init='k-medoids++').fit(X)
        cluster_labels = clusterer.labels_

        cluster_dict = defaultdict(list)

        for id, label in zip(customer_ids, cluster_labels):
            cluster_dict[label].append(id)

        clusters = list(cluster_dict.values())

        with open(feature_selection_path + dc + "/kmedoids.csv", "w") as f:
            wr = csv.writer(f)
            wr.writerows(clusters)

        pickle.dump(clusters, open(feature_selection_path + dc + "/kmedoids.p", "wb"))
        k += 1


if __name__ == "__main__":
    # feature_selection()
    # cluster_plot([14, 14, 13, 14, 4, 14, 14, 14])
    cluster([6, 4, 6, 4, 8, 6, 10, 8], [14, 14, 13, 14, 4, 14, 14, 14])
