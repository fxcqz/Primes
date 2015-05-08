import os
import numpy
import generator
import itertools


class Generator(generator.Generator):
    def __init__(self, minimum=0, maximum=0):
        super(self.__class__, self).__init__(minimum, maximum)
        self.path = "primes/generator/data/big/big_primes.dat"
        self.size = "1 Million"

    def set_size(self, s):
        self.size = s

    def set_specifics(self, data):
        try:
            if data['big']:
                self.set_size(data['big'])
        except KeyError:
            pass

    def size_to_limit(self):
        size = 1000000
        if self.size == "2 Million":
            size = 2000000
        elif self.size == "5 Million":
            size = 5000000
        elif self.size == "10 Million":
            size = 10000000
        return size

    def generate(self):
        if not os.path.exists(self.path):
            self.data = [2]
            return
        lim = self.size_to_limit()
        data = numpy.loadtxt(self.path, delimiter=',')
        self.data = numpy.fromiter(itertools.takewhile(lambda x: x < lim, data), float)
