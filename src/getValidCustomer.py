""" This script get the customers that has at least 1000 requests"""

import os
import pickle
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
output = "/research/yazhuo/ALL_DATA/CDN/clusters/"      #path for store the results

threshold = 1000 # minimum number of requests

def getCustomer():
    for dc in DC:
        print(dc)
        input_path = input + dc + "/"
        output_path = output + dc + "/"
        validCumtomers = []  # a list of customer ids

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        for filename in os.listdir(input_path):
            with open(input_path + filename) as f:
                count = len(f.readlines())
                if count >= threshold:
                    validCumtomers.append(filename)
        with open(output_path + "customerids.txt", "w") as f:
            for id in validCumtomers:
                f.write(id + '\n')
       
       
if __name__ == "__main__":
    getCustomer()
