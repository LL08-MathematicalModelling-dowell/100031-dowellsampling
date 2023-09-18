from API.functions.sampleSize import dowellSampleSize

import random


def dowellClusterSampling(clusterSamplingInput):
    Yi = clusterSamplingInput['Yi']
    N =  clusterSamplingInput['N']                # Initializing population size
    e = clusterSamplingInput['e']                 # Desired margin of error (5%)
    M = clusterSamplingInput['M']                 # Initializing number of clusters
    hi = clusterSamplingInput['hi']               # Initializing size of the cluster
    m = dowellSampleSize(N, e) 
    print("m", m)

    # Divide the whole populaton into clusters of size "hi"
    clusters = [Yi[i : i + hi] for i in range(0, M, hi)]
    print("clusters", clusters)

    # Make sure that clusters are heterogenous by selecting non repeating samples from the cluster.
    ind = [random.randrange(0, len(clusters)) for _ in range(m)]
    print("ind", ind)
    sampled_clusters = [clusters[i] for i in ind]
    print("sampled clusters", sampled_clusters)
    return sampled_clusters

