"""kmeans.py"""
from dis import dis
from operator import index
from random import randint
from functools import reduce
from math import sqrt


class Cluster:
    """This class represents the clusters, it contains the
    prototype (the mean of all it's members) and memberlists with the
    ID's (which are Integer objects) of the datapoints that are member
    of that cluster. You also want to remember the previous members so
    you can check if the clusters are stable."""

    def __init__(self, dim):
        self.prototype = [0.0 for _ in range(dim)]
        self.current_members = set()
        self.previous_members = set()

class KMeans:
    def __init__(self, k, traindata, testdata, dim):
        self.k = k
        self.traindata = traindata
        self.testdata = testdata
        self.dim = dim

        # Threshold above which the corresponding html is prefetched
        self.prefetch_threshold = 0.25
        # An initialized list of k clusters
        self.clusters = [Cluster(dim) for _ in range(k)]

        # The accuracy and hitrate are the performance metrics (i.e. the results)
        self.accuracy = 0
        self.hitrate = 0

    def train(self):
        # random.seed(10)

        # Init
        for i in range(self.k): 
            self.clusters[i].current_members.add(randint(0, len(self.testdata) - 1))
            self.clusters[i].prototype = self.testdata[randint(0, len(self.testdata) - 1)]

        # Assign members to clusters
        for l, i in enumerate(self.testdata):
            distances = [sqrt(reduce(lambda a, b: a + b, [pow(k - j.prototype[idx], 2) for idx, k in enumerate(i)])) for j in self.clusters]
            index_shortest = distances.index(min(distances))
            self.clusters[index_shortest].current_members.add(l)

        optimizing = True

        # Update cluster prototype and cluster members
        while(optimizing):
            for i in self.clusters:
                i.prototype = [reduce(lambda a, b: a + b, [self.testdata[k][j] for k in i.current_members]) / len(i.current_members) for j in range(self.dim)]
                i.previous_members = i.current_members
                i.current_members.clear()

            for l, i in enumerate(self.testdata):
                distances = [sqrt(reduce(lambda a, b: a + b, [pow(k - j.prototype[idx], 2) for idx, k in enumerate(i)])) for j in self.clusters]
                index_shortest = distances.index(min(distances))
                self.clusters[index_shortest].current_members.add(l)

            for i in self.clusters:
                if i.current_members == i.previous_members:
                    optimizing = False
                    break

    def test(self):
        hit_count = 0
        request_count = 0
        prefetched_count = 0
        for client_id, _ in enumerate(self.testdata):
            for i in self.clusters:
                pre_fetched = [1 if j >= self.prefetch_threshold else 0 for j in i.prototype]
                if client_id in i.current_members:
                    hit_count += reduce(lambda a, b: a + b, [1 if self.testdata[client_id][idx] == 1 and k == 1 else 0 for idx, k in enumerate(pre_fetched)])
                    request_count += reduce(lambda a, b: a + b, self.testdata[client_id])
                    prefetched_count += reduce(lambda a, b: a + b, pre_fetched)
        self.hitrate = hit_count / request_count
        self.accuracy = hit_count / prefetched_count
        self.print_test()

    def print_test(self):
        print("Prefetch threshold =", self.prefetch_threshold)
        print("Hitrate:", self.hitrate)
        print("Accuracy:", self.accuracy)
        print("Hitrate+Accuracy =", self.hitrate+self.accuracy)
        print()

    def print_members(self):
        for i, cluster in enumerate(self.clusters):
            print("Members cluster["+str(i)+"] :", cluster.current_members)
            print()

    def print_prototypes(self):
        for i, cluster in enumerate(self.clusters):
            print("Prototype cluster["+str(i)+"] :", cluster.prototype)
            print()