import os
import pickle
from collections import defaultdict
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
import random

# The list of datacenters
DC = ["dc_1384",
      "dc_1448",
      "dc_1731",
      "dc_1831",
    #   "dc_1870",
    #   "dc_189",
    #   "dc_1966",
    #   "dc_1980",
    #   "dc_66",
    #   "dc_67",
    #  "dc_85",
    #   "dc_924"
    #   "lax_1319"
]

input = "/home/yanan/results/"
output = "/home/yanan/results/cdf/"

cluster_path = "/research/yazhuo/ALL_DATA/CDN/clusters/"   

def getValidIDs(dc):  # read the valid cutomer ids
    validIDs = []
    with open(cluster_path + dc + "/customerids.txt", "r") as f:
        for id in f.readlines():
            validIDs.append(id.strip())
    return validIDs


def getCDF():
    for dc in DC:
        print(dc)
        input_path = input + dc + "/"
        output_path = output + dc + "/"
        freq_dic = defaultdict(list)  # key: customer, value: features
        size_dic = defaultdict(list)
        validIDs = getValidIDs(dc)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        freq_all = []
        size_all = []
        max_freq = 0
        max_size = 0
        for filename in os.listdir(input_path):
            customer = filename[:len(filename) - 11]  #get the customer id
            if customer in validIDs:
                filename = input_path + filename
                with open(filename, 'rb') as pickle_file:
                    if "freq" in filename:
                  
                        freq = pickle.load(pickle_file)
                        freqs = []
                        for val in freq.values():
                            for i in range(val):
                                freqs.append(val)

                        freqs = np.array(freqs)

                        freq_all.append(freqs)

                    else:  # size frequence file
                        size = pickle.load(pickle_file)
                        sizes = []
                        for key, val in size.items():
                            for i in range(val):
                                sizes.append(int(key))
                        sizes = np.array(sizes) // 1024

                        size_all.append(sizes)



        for freq in freq_all:
            num_bins = max(freq) - min(freq)
            if num_bins == 0:
                num_bins = 1
            count, bins_count = np.histogram(freq, bins=num_bins)
            pdf = count / sum(count)
            cdf = np.cumsum(pdf)
            plt.plot(bins_count[1:], cdf, linewidth=0.1)
        plt.xlabel("Object Frequency")
        plt.ylabel("CDF")
        plt.xscale('log',base=10)
        plt.savefig(output_path + "freqLog")
        plt.close()

        
        for size in size_all:
            num_bins = max(size) - min(size)
            if num_bins == 0:
                num_bins = 1
            count, bins_count = np.histogram(size, bins=num_bins)
            pdf = count / sum(count)
            cdf = np.cumsum(pdf)
            plt.plot(bins_count[1:], cdf, linewidth=0.1)
        plt.xlabel("Object Size")
        plt.ylabel("CDF")
        plt.xscale('log',base=10)
        plt.savefig(output_path + "sizeLog")
        plt.close()


    
if __name__ == "__main__":
    getCDF()