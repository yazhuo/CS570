# coding=utf-8

from collections import defaultdict
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mmh3
import math
import os
from multiprocessing import Pool
import sys

from splay import SplayTree, node_uniq

DC = [
    "dc_189",
    "dc_924",
    "dc_1384",
    "dc_1448",
    "dc_1731",
    "dc_1831",
    "dc_1870",
    "dc_1966"]


input_dir = "/research/yazhuo/CS570/Dataset/"
output_dir = "/research/yazhuo/CS570/Output/"

DS = [
    "N_dc_1448_6/",
    "F_dc_1448_4/",
    "F_dc_1384_6/"
]

MS = [
    "Kmeans/",
    "Kmedoids/"
]

d_index = 0
m_index = 0
num_trace = 7

###############################################################################
#   Core functions
###############################################################################

def sim_lru_cache(a):

    c = int(a)
    
    if c < num_trace - 1:
        input_file_loc = input_dir +  MS[m_index] + DS[d_index] + "cluster_" + str(c)
        output_file_loc = output_dir + MS[m_index] + DS[d_index] +  "rd_cluster_" + str(c)
    else:
        input_file_loc = input_dir + MS[m_index] + DS[d_index] + "single_trace"
        output_file_loc = output_dir + MS[m_index] + DS[d_index] + "rd_single"

    times, customers, keys, sizes = reader(input_file_loc)

    n = len(times)
    T = SplayTree()
    H = defaultdict(lambda:None)

    rds = []
    for j in range(n):
        rd = cal_req_rd(times[j], keys[j], sizes[j], T, H)
        rds.append(rd)

    save_rds(output_file_loc, rds, customers, c)



def cal_req_rd(t, k, s, T, H):
    """
    Calculate reuse distance for the current item
    """
    if None == H[k]:
        newtree = T.insert(t, s)
        H[k] = t
        rd = -1
    else:
        pre_t = H[k]
        newtree = T.splay(pre_t)
        rd = node_uniq(newtree.right) + s
        H[k] = t
        newtree = T.delete(pre_t)
        newtree = T.insert(t, s)
    
    return rd



###############################################################################
#   Auxiliary functions
###############################################################################

def reader(file_loc):

    df = pd.read_csv(file_loc, sep = '\t', usecols=[0,1,2,3], header=None)
    
    times = df[0].values
    customers = df[1].values
    keys = df[2].values
    sizes = df[3].values
    
    return times, customers, keys, sizes


def save_rds(output_file_loc, rds, customers, c):
    
    print("start store rd in cluster " + str(c))
    w = open(output_file_loc, 'w')

    for i in range(len(rds)):
        w.write(str(customers[i])+ "\t" +  str(rds[i])+ '\n')
        out_cus_rd = output_dir + MS[m_index] + DS[d_index] + "rd_cluster_" + str(c) + "_" + str(customers[i])
        with open(out_cus_rd, 'a+') as fc:
            fc.write(str(rds[i]) + "\n")

    w.close()
    print("finish cluster " + str(c))


if __name__ == "__main__":

    # python3 simulator.py 0 0 7
    # python3 simulator.py 1 0 7
    # python3 simulator.py 1 1 5
    # python3 simulator.py 1 2 7

    m_index = int(sys.argv[1])
    d_index = int(sys.argv[2])
    num_trace = int(sys.argv[3])
    
    print('Parent process %s.' % os.getpid())
    p = Pool(num_trace)
    for i in range(num_trace):
        p.apply_async(sim_lru_cache, args=(i,))
    
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

    os.popen('python3 /research/yazhuo/Tools/send_email.py simulator')