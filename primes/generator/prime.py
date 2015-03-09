__author__ = 'Matt'
import itertools
import math
import generator
import logging
import primes.utils.logger as log
import numpy


logger = logging.getLogger(__name__)

class Generator(generator.Generator):
    def __init__(self, minimum=0, maximum=1):
        super(self.__class__, self).__init__(minimum, maximum)
        self.path = "primes/generator/data/primes/"

    def is_prime(self, n):
        # TODO: use a better primality test
        # http://en.wikipedia.org/wiki/Primality_test
        if n <= 3:
            return n >= 2
        if n % 2 == 0 or n % 3 == 0:
            return False
        for i in range(5, int(n ** 0.5) + 1, 6):
            if n % i == 0 or n % (i + 2) == 0:
                return False
        return True

    def j_increment(self, j):
        return [int(math.pow(j, 2) + (n * j)) for n in
                itertools.takewhile(lambda x: int(math.pow(j, 2) + (x * j)) <= self.maximum, range(0, self.maximum))]

    def generate(self):
        self.data = self.read_cache()
        cache_miss = self.not_in_cache()
        if len(cache_miss[0])+len(cache_miss[1]) < self.threshold:
            for l in cache_miss:
                for n in l:
                    if self.is_prime(n):
                        self.data.append(n)
            self.data.sort()
        else:
            logger.info("Starting prime generation")
            numbers = [True] * (self.maximum + 1)
            for i in range(2, int(math.sqrt(self.maximum))):
                if numbers[i]:
                    for j in self.j_increment(i):
                        numbers[j] = False
            self.data = numpy.array([i for i, j in enumerate(numbers) if j and i > 1])
            self.to_file()
