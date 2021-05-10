""" This script evaluate the performence of KMeans clustering with different K"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict
import pickle
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

K = range(2,16,2)  # range of number of clusters


feature_path = "/research/yazhuo/ALL_DATA/CDN/features/"
freq = "/freqnew.p"
size = "/sizenew.p"
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

    # print(dc, len(validIDs), len(customer_ids))

    return customer_ids, list(attr_dict.values())

def preprocess(X):
    scaler = preprocessing.StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def evaluate():
    sseall1 = []
    sseall2 = []
    for dc in DC:
        customer_ids, attrs = readAttr(dc)
        X = np.array(attrs)
        X = preprocess(X)
        sse1 = []  # Sum of squared distances for Kmeans
        sse2 = []  # Sum of squared distances for Kmedoids
    
        for n_clusters in K:
            
            clusterer1 = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
            clusterer2 = KMedoids(n_clusters=n_clusters, random_state=0).fit(X)
  
            sse1.append(clusterer1.inertia_) 
            sse2.append(clusterer2.inertia_) 

        sseall1.append(sse1)
        sseall2.append(sse2)

    fig = plt.figure(figsize=(20,7))
    fig.add_subplot(121)

    for i,sse in enumerate(sseall1):
        plt.plot(K, sse, label=DC[i])
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    plt.legend()
    fig.add_subplot(122)
    for i,sse in enumerate(sseall2):
        plt.plot(K, sse, label=DC[i])
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    plt.legend()
    plt.savefig(output_path + "/SSE2.png")

  

if __name__ == "__main__":
    evaluate()
