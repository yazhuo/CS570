""" This script provide functions for read attributes, get customer ids and cluster results """
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

feature_path = "/research/yazhuo/ALL_DATA/CDN/features/"
culster_path = "/research/yazhuo/ALL_DATA/CDN/clusters/" 
cluster_path_selection = "/research/yazhuo/ALL_DATA/CDN/selection/" 
freq = "/freq.p"
size = "/size.p"
burst = "/burst.csv"


def getValidIDs(dc):  # read the valid cutomer ids for a datacenter
    validIDs = []
    with open(culster_path + dc + "/customerids.txt", "r") as f:
        for id in f.readlines():
            validIDs.append(id.strip())
    return validIDs

<<<<<<< HEAD
def getCluster(dc):
    with open(culster_path + dc + "/kmedoids.p", 'rb') as pickle_file:
=======
#  get clusters generated from all the features
#  file = '/kmeans.p' or '/kmedoids.p'
def getCluster(dc, file):
    with open(culster_path + dc + file, 'rb') as pickle_file:
>>>>>>> f96e36a8db1f7e0c1ed9c9fa413dcc31df763013
        clusters = pickle.load(pickle_file) # list of list

    return clusters  

# get the clusers generated from selected feature
#  file = '/kmeans.p' or '/kmedoids.p'
def getClusterSelection(dc, file):
    with open(cluster_path_selection + dc + file, 'rb') as pickle_file:
        clusters = pickle.load(pickle_file) # list of list
    return clusters  

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
