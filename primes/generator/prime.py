import itertools
import math
import generator
import logging
import numpy
import primes.utils.primality as primality


logger = logging.getLogger(__name__)

class Generator(generator.Generator):
    """Generate a set of prime numbers up to a given limit using the Sieve of
    Eratosthenes.

    Keyword Arguments:
        minimum -- the minimum value to be used in the dataset (default 0)
        maximum -- the maximum value to be used in the dataset (default 2)
    """
    def __init__(self, minimum=0, maximum=2):
        super(self.__class__, self).__init__(minimum, maximum)
        self.path = "primes/generator/data/primes/"
        if self.minimum < 2 and self.maximum < 2:
            self.runnable = False

    def j_increment(self, j):
        """Helper function for the Sieve of Eratosthenes algorithm.
        
        Returns:
            A list of multiples of the integer j to then be excluded from the
            prime list.
        """
        return [int(math.pow(j, 2) + (n * j)) for n in
                itertools.takewhile(lambda x: int(math.pow(j, 2) + (x * j)) <= self.maximum, range(0, self.maximum))]

    def generate(self):
        """See the stub in the Generator super class for more information."""
        self.data = self.read_cache()
        cache_miss = self.not_in_cache()
        if cache_miss:
            self.data = list(self.data)
            for l in cache_miss:
                for n in l:
                    if primality.is_prime(n):
                        self.data.append(n)
            self.data.sort()
            self.data = numpy.array(self.data)
        else:
            logger.info("Starting prime generation")
            # Sieve of eratosthenes implementation
            numbers = [True] * (self.maximum + 1)
            for i in range(2, int(math.sqrt(self.maximum)) + 1):
                if numbers[i]:
                    for j in self.j_increment(i):
                        numbers[j] = False
            self.data = numpy.array([i for i, j in enumerate(numbers) if j and i > 1])
            self.to_file()
