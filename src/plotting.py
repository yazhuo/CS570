import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
from collections import Counter, defaultdict

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

p_ratio = np.array([
    0.125,
    0.125,
    0.125,
    0.125,
    0.125,
    0.125,
    0.125,
    0.125,
    ])

input_dir = "/research/yazhuo/CS570/Output/K8/dc_1448/variable/"


###############################################################################
#   Plotting
###############################################################################

def plot_cdn_mrcs(single_mrc, partition_mrc, max_cache, step):
    
    x_axis = list(np.arange(0, 1000, 10))
    s_mrc = single_mrc[0:1000:10] 
    p_mrc = partition_mrc[0:1000:10] 

    plt.figure('mrc plot')

    plt.plot(x_axis, s_mrc, label="Unitary Cache")
    plt.plot(x_axis, p_mrc, label="Partitioned Cache")

    plt.xlabel('Cache size (GB)')
    plt.ylabel('Object Miss Rate')
    #plt.xscale('log', basex=2)
    plt.ylim(0,1)
    plt.legend()
    plt.savefig("s_p_mrc.png")


def plot_customer_mrcs(s_mrc, p_mrc):

    x_axis = np.arange(len(s_mrc))


###############################################################################
#   MRC
###############################################################################

def cal_unit_hit_rate(file_loc):
    
    df = pd.read_csv(file_loc, sep = '\t', usecols=[1], header=None)
    rds = df[1].values

    total_req = len(rds)
    
    
    bins = np.arange(-1, max(rds)+2)
    hit_count, bin_edges = np.histogram(rds, bins=bins, density=False)

    hrc = np.cumsum(hit_count[1:])
    max_cache = bins[-1]

    return hrc, max_cache, total_req


def cache_unit_mrc():
    
    file_loc = input_dir + 'rd_single'
    single_hc, max_cache, total_req = cal_unit_hit_rate(file_loc)
    cache_partition = p_ratio * max_cache

    cluster_hc = [[] for i in range(8)]

    for i in range(8):
        print(i)
        file_loc = input_dir + 'rd_cluster_' + str(i)
        hc_np, c, part_num_req = cal_unit_hit_rate(file_loc)

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


def cus_behavior(customer_id, cluster_id, max_cache, step):

    single_rds, partition_rds = read_customer_rds(customer_id, cluster_id)
    total_req = len(single_rds)

    max_partition = p_ratio[0] * max_cache
    step_partition = p_ratio[0] * step

    single_bins = np.arange(0, max_cache, step)
    part_bins = np.arange(0, max_partition, step_partition)
    single_hit_rate, bin_edges = np.histogram(single_rds, bins=single_bins, density=False)
    partition_hit_rate, bin_edges = np.histogram(partition_rds, bins=part_bins, density=False)

    print(single_hit_rate)
    print(bin_edges)

    single_hrc = np.cumsum(single_hit_rate)
    partition_hrc = np.cumsum(partition_hit_rate)

    single_mrc = 1 - single_hrc/total_req
    partition_mrc = 1 - partition_hrc/total_req

    return single_mrc, partition_mrc



def cal_variable_hit_rate(file_loc, max_cache, step):
    
    df = pd.read_csv(file_loc, sep = '\t', usecols=[1], header=None)
    rds = df[1].values  

    total_req = len(rds)
    total_size = sum(list(rds))

    bins = np.arange(0, max_cache, step)
    hit_count, bin_edges = np.histogram(rds, bins=bins, density=False)
    hit_byte_count = hit_count * bins[1:]

    hc = np.cumsum(hit_count)
    hbc = np.cumsum(hit_byte_count)
    
    return hc, hbc, total_req, total_size


def cache_variable_mrc(max_cache, step):
    file_loc = input_dir + 'rd_single'
    single_hc, single_byte_hc, total_req, total_size = cal_variable_hit_rate(file_loc, max_cache, step)
    max_partition = p_ratio * max_cache

    cluster_hc = [[] for i in range(8)]
    cluster_byte_hc = [[] for i in range(8)]

    for i in range(8):
        print(i)
        file_loc = input_dir + 'rd_cluster_' + str(i)
        partition_hc, partition_byte_hc, partition_req, partition_size = cal_variable_hit_rate(file_loc, max_partition[i], step)
        hc = list(partition_hc)
        byte_hc = list(partition_byte_hc)
        cluster_hc[i].extend(hc)
        cluster_byte_hc[i].extend(byte_hc)

        last_c = cluster_hc[i][-1]
        last_part = [last_c for j in range(len(hc), max_cache, step)]
        cluster_hc[i].extend(last_part)

        # byte_last_c = cluster_byte_hc[i][-1]
        # byte_last_part = [last_c for j in range(len(byte_hc), max_cache, step)]
        # cluster_byte_hc[i].extend(byte_last_part)
    
    cluster_hc = np.array(cluster_hc, dtype="object")
    part_hc = np.sum(cluster_hc, axis=0)

    # cluster_byte_hc = np.array(cluster_byte_hc, dtype="object")
    # part_byte_hc = np.sum(cluster_byte_hc, axis=0)


    single_mrc = list((total_req - np.array(single_hc)) / total_req)
    partition_mrc = list((total_req - np.array(part_hc)) / total_req)

    # single_bmrc = list((total_size - np.array(single_byte_hc)) / total_size)
    # partition_bmrc = list((total_size - np.array(part_byte_hc)) / total_size)


    print(single_mrc[0:1000:10])
    print(partition_mrc[0:1000:10])

    # print(single_bmrc[0:1000:10])
    # print(partition_bmrc[0:1000:10])
    
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


def read_customer_rds(customer_id, cluster_id):

    file_loc1 = input_dir + "rd_cluster_8_" + str(customer_id)
    df1 = pd.read_csv(file_loc1, sep = '\t', usecols=[0], header=None)
    single_rds = df1[0].values

    # index = [i for i,x in enumerate(customers) if x == c]
    # single_rds = rds[index]

    file_loc2 = input_dir + "rd_cluster_" + str(cluster_id) + "_" + str(customer_id)
    df2 = pd.read_csv(file_loc2, sep = '\t', usecols=[0], header=None)
    partition_rds = df2[0].values
    
    return single_rds, partition_rds


if __name__ == "__main__":

    # single_mrc, partition_mrc = cache_unit_mrc()
    # plot_cdn_mrcs(single_mrc, partition_mrc)

    max_cache = 1024 * 1024 * 1024 * 1024
    step = 1024 * 1024

    # print('calculate cdn mrc')
    # single_mrc, partition_mrc = cache_variable_mrc(max_cache, step)

    # print('plotting object miss rate')
    # plot_cdn_mrcs(single_mrc, partition_mrc, max_cache, step)

    print('calculate customer mrc')
    # 1255, 0
    # 943, 4
    # 1066, 4
    # 601, 1
    customer_id = 241
    cluster_id = 3
    single_mrc, partition_mrc = cus_behavior(customer_id, cluster_id, max_cache, step)
    print(single_mrc)
    print(partition_mrc)
    plot_cdn_mrcs(single_mrc, partition_mrc, max_cache, step)
