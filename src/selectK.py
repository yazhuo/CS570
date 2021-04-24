""" This script evaluate the performence of KMeans clustering with different K"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict
import pickle

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

K = range(2,16,2)  # range of number of clusters


feature_path = "/research/yazhuo/ALL_DATA/CDN/features/"
freq = "/freq.p"
size = "/size.p"
burst = "/burst.csv"

output_path = "/research/yazhuo/ALL_DATA/CDN/clusters/"   # store the cluster performence result

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
            # if row[0] in validIDs:  # only keep the valid customers
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

def evaluate(dc, X):
    sse = []  # Sum of squared distances
    ss = []   # Silhouette score
    
    for n_clusters in K:
        
        clusterer = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
        cluster_labels = clusterer.labels_
        silhouette_avg = silhouette_score(X, cluster_labels)
        ss.append(silhouette_avg)
        sse.append(clusterer.inertia_) 

    fig = plt.figure(figsize=(14,7))
    fig.add_subplot(121)
    plt.plot(K, sse)
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    fig.add_subplot(122)
    plt.plot(K, ss)
    plt.xlabel("Number of cluster")
    plt.ylabel("Silhouette Score")
    plt.savefig(output_path + dc + "/selectk.png")

   

if __name__ == "__main__":
    for dc in DC:
        customer_ids, attrs = readAttr(dc)
        X = np.array(attrs)
        X = preprocess(X)
        evaluate(dc, X)

