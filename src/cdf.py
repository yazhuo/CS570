
""" This script calculate the CDF of object frequence and object size frequence and pick 50% and 99% value as features."""

import os
import pickle
from collections import defaultdict
import sys
import numpy as np
import csv

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

# input = "results/"
# output = "features/"
input = "/home/yanan/results/"
output = "/research/yazhuo/ALL_DATA/CDN/features/"


def getCDF():
    for dc in DC:
        input_path = input + dc + "/"
        freq_dic = defaultdict(list)  # key: customer, value: features
        size_dic = defaultdict(list)

        for filename in os.listdir(input_path):
            customer = filename[:len(filename) - 11]  #get the customer id
            filename = input_path + filename
            with open(filename, 'rb') as pickle_file:
                if "freq" in filename:
                    freq = pickle.load(pickle_file)
                    freqs = []
                    for val in freq.values():
                        for i in range(val):
                            freqs.append(val)

                    freqs = np.array(freqs)
                    # freqs = np.sort(freqs)
                    num_bins = max(freqs) - min(freqs)
                    if num_bins == 0:
                        num_bins = 1
                    count, bins_count = np.histogram(freqs, bins=num_bins)
                    pdf = count / sum(count)
                    cdf = np.cumsum(pdf)

                    idx10 = np.argmax(cdf>=0.10)
                    idx30 = np.argmax(cdf>=0.30)
                    idx50 = np.argmax(cdf>=0.50)
                    idx70 = np.argmax(cdf>=0.70)
                    idx99 = np.argmax(cdf>=0.99)
                    freq_dic[customer] = [bins_count[idx10], bins_count[idx30], bins_count[idx50], bins_count[idx70], bins_count[idx99]]
                else:  # size frequence file
                    size = pickle.load(pickle_file)
                    sizes = []
                    for key, val in size.items():
                        for i in range(val):
                            sizes.append(int(key))
                    sizes = np.array(sizes)
                    # sizes = np.sort(sizes)
            
                    num_bins = max(sizes) - min(sizes)
                    if num_bins == 0:
                        num_bins = 1                  
                    count, bins_count = np.histogram(sizes, bins=num_bins)
                    pdf = count / sum(count)
                    cdf = np.cumsum(pdf)
                    idx10 = np.argmax(cdf>=0.10)
                    idx30 = np.argmax(cdf>=0.30)
                    idx50 = np.argmax(cdf>=0.50)
                    idx70 = np.argmax(cdf>=0.70)
                    idx99 = np.argmax(cdf>=0.99)
                    size_dic[customer] = [bins_count[idx10], bins_count[idx30], bins_count[idx50], bins_count[idx70], bins_count[idx99]]
        # write results 
        output_path = output + dc + "/"
        pickle.dump(freq_dic, open(output_path + "freqnew.p", "wb"))
        pickle.dump(size_dic, open(output_path + "sizenew.p", "wb"))


if __name__ == "__main__":
    getCDF()