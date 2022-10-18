## Caden Kamminga (s4370732)
## Tex McGinley (s4299035)
## Daniel Gentile (s4273389)
from random import randint, random
from math import sqrt
from functools import reduce
from itertools import chain
from statistics import mean
from random import shuffle
from math import exp


class Cluster:
    """This class represents the clusters, it contains the
    prototype and a set with the ID's (which are Integer objects)
    of the datapoints that are member of that cluster."""

    def __init__(self, dim, x, y):
        self.prototype = [random() for _ in range(dim)]
        self.current_members = set()
        self.location = [x, y]


class Kohonen:
    def __init__(self, n, epochs, traindata, testdata, dim):
        self.n = n
        self.epochs = epochs
        self.traindata = traindata
        self.testdata = testdata
        self.dim = dim

        # A 2-dimensional list of clusters. Size == N x N
        self.clusters = [[Cluster(dim, i, j) for i in range(n)] for j in range(n)]
        # Threshold above which the corresponding html is prefetched
        self.prefetch_threshold = 0.5
        self.initial_learning_rate = 0.9
        # The accuracy and hitrate are the performance metrics (i.e. the results)
        self.accuracy = 0
        self.hitrate = 0

    def random_vector(self):
        index = randint(0, len(self.traindata) - 1)
        vector = self.traindata[index]
        return index, vector

    def log_progress(self, current_epoch):
        single_bar = 1 / self.epochs
        bar_count = current_epoch * single_bar * 50
        if current_epoch == self.epochs:
            print('[' + int(bar_count) * '=' + '>' + '.' * int(50 - int(bar_count)) + f'] {current_epoch} / {self.epochs}', end="\n")
        else:
            print('[' + int(bar_count) * '=' + '>' + '.' * int(50 - int(bar_count)) + f'] {current_epoch} / {self.epochs}', end="\r")

    def train(self):
        for epoch_count in range(self.epochs):

            # Update learning rate
            self.initial_learning_rate = 0.8 * (1 - (epoch_count / self.epochs))

            # Clear current members each epoch
            for i in chain.from_iterable(self.clusters): i.current_members.clear()

            ## Loop through each of the clients in the training data
            for idx, i in enumerate(self.traindata):

                # Finding the BMU cluster for a given client using the smalles euclidean distance
                distances = list(chain.from_iterable([[sqrt(reduce(lambda a, b: a + b, [pow(k - m.prototype[idx], 2) for idx, k in enumerate(i)])) for m in j]for j in self.clusters]))
                index_shortest = distances.index(min(distances))
                bmu_node = list(chain.from_iterable(self.clusters))[index_shortest]
                bmu_node.current_members.add(idx)

                ## Finding the neighbors of a BMU cluster and updating the BMU cluster and all its neighbors accordingly
                neighborhood_r = (self.n / 2) * (1 - (epoch_count / self.epochs))
                for node in list(chain.from_iterable(self.clusters)):
                    node_to_bmu = sqrt(reduce(lambda a, b: a + b, [pow(k - node.location[idx], 2) for idx, k in enumerate(bmu_node.location)]))
                    if node_to_bmu <= neighborhood_r:
                        node.prototype = [(1 - self.initial_learning_rate) * j + self.initial_learning_rate * i[idx2] for idx2, j in enumerate(node.prototype)]

            self.log_progress(epoch_count + 1)

    def test(self):
        hit_count = 0
        request_count = 0
        prefetched_count = 0
        # Looping through all the clients in the test data and checking which cluster a client belongs to.
        # Calculating the hit count, request count and prefetched count. Which can be used to calculate the hitrate
        # and accuracy.
        for client_id, _ in enumerate(self.testdata):
            for i in list(chain.from_iterable(self.clusters)):
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
        for i in range(self.n):
            for j in range(self.n):
                print("Members cluster[" + str(i) + "][" + str(j) + "] :", self.clusters[i][j].current_members)
                print()

    def print_prototypes(self):
        for i in range(self.n):
            for j in range(self.n):
                print("Prototype cluster[" + str(i) + "][" + str(j) + "] :", self.clusters[i][j].prototype)
                print()
