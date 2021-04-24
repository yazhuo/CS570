""" This script count the frequence of each object in each customer and the frequence of object size for each customer."""

import os
import pickle
from collections import defaultdict
import sys


# The list of datacenters
DC = ["dc_1384",
      "dc_1448",
      "dc_1731",
      "dc_1831",
      "dc_1870",
      "dc_189",
      "dc_1966",
    #   "dc_1980",
      "dc_66",
    #   "dc_67",
      "dc_85",
      "dc_924"
    #   "lax_1319"
]


input = "/research/yazhuo/ALL_DATA/CDN/splitCustomer/"  #path of the customer files
output = "/home/yanan/results/"                         #path for store the results

def countFreq():
    for dc in DC:
        input_path = input + dc + "/"
        output_path = output + dc + "/"
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        for filename in os.listdir(input_path):
            freq_dict = defaultdict(int)  # key: object id, value: frequence
            size_dict = defaultdict(int)  # key: object size, value: frequence
            with open(input_path + filename) as f:
                for line in f.readlines():
                    request = line.strip().split('\t')
                    object = request[4]
                    object_size = request[5]
                    freq_dict[object] += 1
                    size_dict[object_size] += 1
            pickle.dump(freq, open(output_path + filename + "_obj_freq.p", "wb")) #result file name: customerid_obj_freq.p
            pickle.dump(size, open(output_path + filename + "_obj_size.p", "wb"))

if __name__ == "__main__":
    countFreq()
