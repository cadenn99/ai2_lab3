## Caden Kamminga (s4370732)
## Tex McGinley (s4299035)
## Daniel Gentile (s4273389)

"""kmeans.py"""
from random import randint
from functools import reduce
from math import sqrt
from random import shuffle

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
        self.prefetch_threshold = 0.5
        # An initialized list of k clusters
        self.clusters = [Cluster(dim) for _ in range(k)]

        # The accuracy and hitrate are the performance metrics (i.e. the results)
        self.accuracy = 0
        self.hitrate = 0

    def train(self):

        # Init
        # Creation of random clusters with weights from a random partition of the test.dat file
        random_indexes = [i for i in range(len(self.testdata))]
        shuffle(random_indexes)
        for i in range(self.k):
            member = random_indexes.pop(1)
            self.clusters[i].current_members.add(member)
            self.clusters[i].prototype = self.testdata[member]

        # Assign members to clusters
        # Looping through calculating the Euclidean distance for each client and assigning each client to the cluster
        # with the closest Euclidean distance.
        for l, i in enumerate(self.testdata):
            distances = [sqrt(reduce(lambda a, b: a + b, [pow(k - j.prototype[idx], 2) for idx, k in enumerate(i)])) for j in self.clusters]
            index_shortest = distances.index(min(distances))
            self.clusters[index_shortest].current_members.add(l)

        optimizing = True

        # Update cluster prototype and cluster members
        while optimizing:
            # Finding the new cluster center and clearing all the members from the cluster
            for i in self.clusters:
                i.prototype = [reduce(lambda a, b: a + b, [self.testdata[k][j] for k in i.current_members]) / len(i.current_members) for j in range(self.dim)]
                i.previous_members = i.current_members
                i.current_members.clear()

            # Reassigning all the members to the closest cluster center
            for l, i in enumerate(self.testdata):
                distances = [sqrt(reduce(lambda a, b: a + b, [pow(k - j.prototype[idx], 2) for idx, k in enumerate(i)]))for j in self.clusters]
                index_shortest = distances.index(min(distances))
                self.clusters[index_shortest].current_members.add(l)

            # Checks if the current members and previous members are the same, then a stable point has been found
            for i in self.clusters:
                if i.current_members == i.previous_members:
                    optimizing = False
                    break

    def test(self):
        hit_count = 0
        request_count = 0
        prefetched_count = 0
        # Looping through all the clients in the test data and checking which cluster a client belongs to.
        # Calculating the hit count, request count and prefetched count. Which can be used to calculate the hitrate
        # and accuracy.
        for client_id, _ in enumerate(self.testdata):
            for i in self.clusters:
                pre_fetched = [1 if j >= self.prefetch_threshold else 0 for j in i.prototype]
                if client_id in i.current_members:
                    hit_count += reduce(lambda a, b: a + b, [1 if self.testdata[client_id][idx] == 1 and k == 1 else 0 for idx, k in enumerate(pre_fetched)])
                    request_count += reduce(lambda a, b: a + b, self.testdata[client_id])
                    prefetched_count += reduce(lambda a, b: a + b, pre_fetched)
        self.hitrate = hit_count / request_count
        self.accuracy = hit_count / prefetched_count

    def print_test(self):
        print("Prefetch threshold =", self.prefetch_threshold)
        print("Hitrate:", self.hitrate)
        print("Accuracy:", self.accuracy)
        print("Hitrate+Accuracy =", self.hitrate + self.accuracy)
        print()

    def print_members(self):
        for i, cluster in enumerate(self.clusters):
            print("Members cluster[" + str(i) + "] :", cluster.current_members)
            print()

    def print_prototypes(self):
        for i, cluster in enumerate(self.clusters):
            print("Prototype cluster[" + str(i) + "] :", cluster.prototype)
            print()
