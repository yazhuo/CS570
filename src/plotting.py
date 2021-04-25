import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy

DC = [
    "dc_189",
    "dc_924",
    "dc_1384",
    "dc_1448",
    "dc_1731",
    "dc_1831",
    "dc_1870",
    "dc_1966"]

p_ratio = np.array([
    0.02298,
    0.37063,
    0.00012,
    0.00092,
    0.51231,
    0.09269,
    0.00025,
    0.00005,
    ])

input_dir = "/research/yazhuo/CS570/Output/K8/dc_1448/"



###############################################################################
#   Plotting
###############################################################################

def plot_cdn_mrcs(s_mrc, p_mrc):
    
    x_axis = np.arange(100)

    plt.figure('mrc plot')

    plt.plot(x_axis, s_mrc, label="Unitary Cache")
    plt.plot(x_axis, p_mrc, label="Partitioned Cache")

    plt.xlabel('Cache size (GB)')
    plt.ylabel('Object Miss Rate')
    plt.ylim(0,1)
    plt.legend()
    plt.savefig("s_p_mrc.png", bbox_inches='tight')


def plot_customer_mrcs(s_mrc, p_mrc):

    x_axis = np.arange(len(s_mrc))


###############################################################################
#   MRC
###############################################################################

def cal_hit_rate(file_loc):
    
    df = pd.read_csv(file_loc, sep = '\t', usecols=[1], header=None)
    rds = df[1].values

    total_req = 65950901
    
    bins = np.arange(-1, max(rds)+2)
    hit_count, bin_edges = np.histogram(rds, bins=bins, density=False)

    hrc = np.cumsum(hit_count[1:])
    max_cache = bins[-1]

    return hrc, max_cache, total_req


def cache_mrc():
    
    file_loc = input_dir + 'rd_single'
    single_hc, max_cache, total_req = cal_hit_rate(file_loc)
    cache_partition = p_ratio * max_cache

    cluster_hc = [[] for i in range(8)]

    for i in range(8):
        print(i)
        file_loc = input_dir + 'rd_cluster_' + str(i)
        hc_np, c, part_num_req = cal_hit_rate(file_loc)

        hc = list(hc_np)
        cluster_hc[i].extend(hc)

        last_c = cluster_hc[i][-1]
        last_part = [last_c for j in range(len(hc), max_cache)]
        cluster_hc[i].extend(last_part)
        #print(cluster_hc[i])
    
    cluster_hc = np.array(cluster_hc, dtype="object")
    partition_hc = np.sum(cluster_hc, axis=0)


    single_mrc = list((total_req - np.array(single_hc[0:10000:100])) / total_req)
    partition_mrc = list((total_req - np.array(partition_hc[0:10000:100])) / total_req)

    # print(single_mrc)
    # print(partition_mrc)
    
    return single_mrc, partition_mrc


def cus_behavior(c):

    single_rds, partition_rds = read_customer_rds(c)

    bins = np.arange(-1, max(single_rds)+2)
    single_hit_rate, bin_edges = np.histogram(single_rds, bins=bins, density=True)
    partition_hit_rate, bin_edges = np.histogram(partition_rds, bins=bins, density=True)

    single_hrc = np.cumsum(single_hit_rate[1:])
    partition_hrc = np.cumsum(partition_hit_rate[1:])

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


def read_customer_rds(c):

    file_loc1 = input_dir + "rd_single"
    df = pd.read_csv(file_loc1, sep = '\t', usecols=[0,1], header=None)
    customers = df[0].values
    rds = df[1].values

    index = [i for i,x in enumerate(customers) if x == c]
    single_rds = rds[index]

    file_loc2 = input_dir + "cluster_0_" + str(c)
    df = pd.read_csv(file_loc2, sep = '\t', usecols=[1], header=None)
    partition_rds = df[0].values
    
    return single_rds, partition_rds

if __name__ == "__main__":

    single_mrc, partition_mrc = cache_mrc()
    plot_cdn_mrcs(single_mrc, partition_mrc)