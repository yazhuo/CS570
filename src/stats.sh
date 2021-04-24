#!/bin/bash

a=($(wc -l /research/yazhuo/CS570/Dataset/K8/dc_1448/single_cache_trace))

for i in 0 1 2 3 4 5 6 7
do
    b=($(wc -l /research/yazhuo/CS570/Dataset/K8/dc_1448/cluster_$i))
    echo "scale=5; p = ${b[0]} / ${a[0]}; if (length(p)==scale(p)) print 0;print p" |bc;echo
done

# 0.02298
# 0.37063
# 0.00012
# 0.00092
# 0.51231
# 0.09269
# 0.00025
# 0.00005