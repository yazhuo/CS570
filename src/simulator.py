# coding=utf-8

from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mmh3
import math

from splay import SplayTree, node_uniq

HDC = [
      "dc_1448",
      "dc_1831",
      "dc_1870",
      "dc_924",
      "dc_1731",
      "dc_189",
      "dc_1966",
      "dc_66",
      "dc_85",
      "dc_1384"]

DC = [
      "dc_1448",
      "dc_1831",
      "dc_1870",
      "dc_924",
      "dc_1731",
      "dc_189",
      "dc_1966",
      "dc_66",
      "dc_85",
      "dc_1384"]

# representative customers in each DC
agents = []
clusters = [[0,12], [63,66]]

hetero_dc_path = "/research/jason/ALL_DATA/akamai4/csv/"
split_dc_path = "/research/yazhuo/ALL_DATA/CDN/splitCustomer/"


###############################################################################
#   Core functions
###############################################################################


def single_cache():
    pass


def partitioned_cache():
    pass


###############################################################################
#   Auxiliary functions
###############################################################################

def reader():

    pass


def save_rds():
    pass


def read_rds():
    pass


if __name__ == "__main__":

    pass