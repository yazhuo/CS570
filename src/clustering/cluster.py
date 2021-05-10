""" This script culsters the customers using 3 clustering algorithms"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict
import pickle
from sklearn.cluster import KMeans, DBSCAN
from sklearn_extra.cluster import KMedoids


# The list of datacenters
DC = ["dc_1384",
      "dc_1448",
      "dc_1731",
      "dc_1831",
      "dc_1870",
      "dc_189",
      "dc_1966",
      "dc_924"
]


feature_path = "/research/yazhuo/ALL_DATA/CDN/features/"
freq = "/freqnew.p"
size = "/sizenew.p"
burst = "/burst.csv"

output_path = "/research/yazhuo/ALL_DATA/CDN/clusters/"   # store the cluster result, named as the clustering function

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
                for val in row[-10:]:  # only keep the last 10 time window
                        attr_dict[row[0]].append(int(val))
    
    # read and append freqency 
    with open(feature_path + dc + freq, 'rb') as pickle_file:
        freq_dict = pickle.load(pickle_file)
    
        for key, vals in freq_dict.items():
            for val in vals:
                if key in attr_dict.keys(): # only keep the valid customers
                    attr_dict[key].append(val)


    # read and append size 
    with open(feature_path + dc + size, 'rb') as pickle_file:
        size_dict = pickle.load(pickle_file)
        for key, vals in size_dict.items():
                for val in vals:
                    if key in attr_dict.keys(): # only keep the valid customers
                        attr_dict[key].append(val)


    customer_ids = attr_dict.keys()

    print(dc, len(validIDs), len(customer_ids))

    return customer_ids, list(attr_dict.values())

def preprocess(X):
    scaler = preprocessing.StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def clustering():
    out_file_names_csv = ["/kmeans.csv", "/kmedoids.csv", "/DBSCAN.csv"]
    out_file_names = ["/kmeans.p", "/kmedoids.p", "/DBSCAN.p"]
    n_clusters = 6
    for dc in DC:
        customer_ids, attrs = readAttr(dc)
        X = np.array(attrs)
        X = preprocess(X)

        KmeansClusterer = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
        KMedoidsClusterer = KMedoids(n_clusters=n_clusters, random_state=0).fit(X)
        DBSCANClusterer = DBSCAN(eps=3, min_samples=2).fit(X)
        clusterers = [KmeansClusterer, KMedoidsClusterer, DBSCANClusterer]

        for clusterer, file_name_csv,file_name in zip(clusterers, out_file_names_csv,out_file_names):
            cluster_labels = clusterer.labels_

            cluster_dict = defaultdict(list)

            for id, label in zip(customer_ids, cluster_labels):
                cluster_dict[label].append(id)

            clusters = list(cluster_dict.values())

            with open(output_path + dc + file_name_csv,"w") as f:
                wr = csv.writer(f)
                wr.writerows(clusters)

            pickle.dump(clusters, open(output_path + dc + file_name, "wb"))

   

if __name__ == "__main__":
    clustering()

