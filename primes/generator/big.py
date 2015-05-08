import os
import numpy
import generator
import itertools


class Generator(generator.Generator):
    """Static generator exclusively for working with large datasets.

    This generator  reads  from a file which  has been generated  externally and
    will not generate or cache any new data itself. The minimum and maximum args
    received from Generator are not used and are  simply present for inheritence
    reasons.
    """
    def __init__(self, minimum=0, maximum=0):
        super(self.__class__, self).__init__(minimum, maximum)
        self.path = "primes/generator/data/big/big_primes.dat"
        self.size = "1 Million"

    def set_size(self, s):
        self.size = s

    def set_specifics(self, data):
        """Used to set the value representing the limit of the dataset desired."""
        try:
            if data['big']:
                self.set_size(data['big'])
        except KeyError:
            pass

    def size_to_limit(self):
        """Converts the string obtained from the gui into an integer."""
        size = 1000000
        if self.size == "2 Million":
            size = 2000000
        elif self.size == "5 Million":
            size = 5000000
        elif self.size == "10 Million":
            size = 10000000
        return size

    def generate(self):
        """Reads a pre-defined amount of data from the cache."""
        if not os.path.exists(self.path):
            self.data = [2]
            return
        lim = self.size_to_limit()
        data = numpy.loadtxt(self.path, delimiter=',')
        self.data = numpy.fromiter(itertools.takewhile(lambda x: x < lim, data), float)
