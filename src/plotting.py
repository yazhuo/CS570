import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

DC = [
    "dc_189",
    "dc_924",
    "dc_1384",
    "dc_1448",
    "dc_1731",
    "dc_1831",
    "dc_1870",
    "dc_1966"]

p_ratio = np.array([0.5, 0.5])

input_dir = "/research/yazhuo/CS570/Output/K8/dc_1448/"



###############################################################################
#   Plotting
###############################################################################

def plot():
    pass


###############################################################################
#   MRC
###############################################################################

def cal_hit_rate(file_loc):
    
    df = pd.read_csv(file_loc, sep = ' ', usecols=[1], header=None)
    rds = df[1].values
    
    bins = np.arange(-1, max(rds)+2)
    hit_rate, bin_edges = np.histogram(rds, bins=bins, density=True)

    hrc = np.cumsum(hit_rate[1:])
    max_cache = bins[-1]

    return hrc, max_cache


def cache_mrc():
    
    file_loc = input_dir + 'rd_single'
    single_hrc, max_cache = cal_hit_rate(file_loc)

    cache_partition = p_ratio * max_cache

    cluster_hrc = [[0 for i in range(max_cache)] for i in range(9)]

    for i in range(9):
        file_loc = input_dir + 'rd_cluster_' + str(i)
        hrc, c = cal_hit_rate(file_loc)
        
        newcachesize = int(cache_partition[i])
        for j in range(newcachesize+1):
            cluster_hrc[i][j] = hrc[j]


    partition_hrc = np.sum(cluster_hrc, axis=0)
    
    single_mrc = 1 - single_hrc
    partition_mrc = 1 - partition_hrc
    
    return single_mrc, partition_mrc



###############################################################################
#   Auxiliary functions
###############################################################################

def read_rds():

    rd_file_loc = input_dir
    f = open(rd_file_loc, 'r')

    rds = []
    for line in f.readlines():  
        rds.append(int(line.strip()))

    f.close()

    return rds


def read_customer_rds():
    pass



if __name__ == "__main__":

    cache_mrc()