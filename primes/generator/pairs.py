import numpy
import prime
import generator
import logging
import primes.utils.primality as primality
import time


#logger = logging.getLogger(__name__)

class Generator(generator.Generator):
    def __init__(self, minimum=0, maximum=2):
        super(self.__class__, self).__init__(minimum, maximum)
        self.path = "primes/generator/data/pairs/"
        self.threshold = 500
        sieve = prime.Generator(maximum=self.maximum)
        sieve.generate()
        self.primes = sieve.data
        self.gap = 0

    def set_gap(self, n):
        self.gap = n

    def generate(self):
        self.path += str(self.gap) + "/"
        #logger.info("Checking cache")
        self.data = self.read_cache()
        cache_miss = self.not_in_cache()
        if cache_miss:
            for l in cache_miss:
                for v in l:
                    if primality.is_prime(v) and primality.is_prime(v-self.gap):
                        self.data.append(v)
            self.data.sort()
        else:
            for i, p in enumerate(self.primes):
                if (p - self.gap) in self.primes[:i]:
                    self.data.append(p)
            self.data.sort()
            self.to_file()
