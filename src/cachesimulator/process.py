import pandas as pd
import numpy as np
import os
from multiprocessing import Pool
import sys

from utils import getCluster, getClusterSelection

input_dir = "/research/jason/ALL_DATA/akamai4/csv/"

DC = [
    "lax_1448",
    "sjc_1384"
]

out_DC = [
    "dc_1448",
    "dc_1384"
]

dc_index = 0
num_cluster = 0
method = ""
feature = ""

input_dir = "/research/jason/ALL_DATA/akamai4/csv/"
output_dir = "/research/yazhuo/CS570/Dataset/"



def find_index(c, clusters):

    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            if clusters[i][j] == str(c):
                return i
    return -1


def processbyDC(d):

    dc = out_DC[d]
    clusters = getCluster(dc)

    trace_path = input_dir + DC[d]
    output_dc_path = output_dir + out_DC[d]
    
    df = pd.read_csv(trace_path, sep = '\t', usecols=[0,3,5,9], header=None)
    times = df[0].values
    cus = df[3].values
    keys = df[5].values
    sizes = df[9].values

    n = len(times)
    out_loc = output_dir + out_DC[d] + "/single_cache_trace"
    w = open(out_loc, 'a+')

    for i in range(n):
        g = find_index(cus[i], clusters)
        if g > -1:
            w.write(str(times[i]) + "\t" + str(cus[i]) + "\t" + str(keys[i]) + "\t" + str(sizes[i]) +  "\n")
            out_g_loc = output_dir + out_DC[d] + "/cluster_" + str(g)
            with open(out_g_loc, 'a+') as fg:
                fg.write(str(times[i]) + "\t" + str(cus[i]) + "\t" + str(keys[i]) + "\t" + str(sizes[i]) +  "\n")
    w.close()



def processbyCluster(k):

    if feature == "N":
        if method == "Kmeans":
            clusters = getCluster(out_DC[dc_index], "/kmeans.p")
        else:
            clusters = getCluster(out_DC[dc_index], "/kmedoids.p")
    else:
        clusters = getClusterSelection(out_DC[dc_index], "/kmedoids.p")
    
    if k < num_cluster:
        customers = clusters[k]
    
    trace_path = input_dir + DC[dc_index]
    output_dc_path = output_dir + method + "/" + feature + "_" + out_DC[dc_index] + "_" + str(num_cluster) + "/"


    df = pd.read_csv(trace_path, sep = '\t', usecols=[0,3,5,9], header=None)
    times = df[0].values
    cus = df[3].values
    keys = df[5].values
    sizes = df[9].values

    n = len(times)

    if k < num_cluster:
        out_loc = output_dc_path + "cluster_" + str(k)
        w = open(out_loc, 'a+') 

        for i in range(n):
            if str(cus[i]) in customers:
                w.write(str(times[i]) + "\t" + str(cus[i]) + "\t" + str(keys[i]) + "\t" + str(sizes[i]) +  "\n")
        w.close()
    else:
        out_loc = output_dc_path + "single_trace"
        w = open(out_loc, 'a+') 
        for i in range(n):
            g = find_index(cus[i], clusters)
            if g > -1:
                w.write(str(times[i]) + "\t" + str(cus[i]) + "\t" + str(keys[i]) + "\t" + str(sizes[i]) +  "\n")
        w.close()



if __name__ == "__main__":

    # python3 process.py 0 6 Kmeans N
    # python3 process.py 0 6 Kmedoids N

    # python3 process.py 0 4 Kmedoids F
    # python3 process.py 1 6 Kmedoids F

    dc_index = int(sys.argv[1])
    num_cluster = int(sys.argv[2])
    method = sys.argv[3]
    feature = sys.argv[4]

    # process one DC in parallel
    print('Parent process %s.' % os.getpid())
    p = Pool(num_cluster + 1)
    for i in range(num_cluster + 1):
        p.apply_async(processbyCluster, args=(i,))
    print("waiting for all subprocesses done...")
    p.close()
    p.join()
    print('All subprocesses done')
    
    os.popen('python3 /research/yazhuo/Tools/send_email.py process')
