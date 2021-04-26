import pandas as pd
import numpy as np
import os
from multiprocessing import Pool

from utils import getValidIDs, getCluster

input_dir = "/research/jason/ALL_DATA/akamai4/csv/"

DC = [
    "nyc_189",
    "lax_924",
    "lax_1831",
    "lax_1448",
    "nyc_1731",
    "lax_1831",
    "lax_1870",
    "nyc_1966"
]

out_DC = [
    "dc_189",
    "dc_924",
    "dc_1384",
    "dc_1448",
    "dc_1731",
    "dc_1831",
    "dc_1870",
    "dc_1966"
]

input_dir = "/research/jason/ALL_DATA/akamai4/csv/"
output_dir = "/research/yazhuo/CS570/Dataset/K8/"


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



if __name__ == "__main__":

    print('Parent process %s.' % os.getpid())
    num_DC = len(out_DC)
    p = Pool(num_DC)
    for i in range(num_DC+1):
        p.apply_async(processbyDC, args=(i,))
    
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

    
    os.popen('python3 /research/yazhuo/Tools/send_email.py')
