__author__ = 'Matt'
import itertools
import math
import generator
import logging
import primes.utils.logger as log


log.setup_logging()
logger = logging.getLogger(__name__)

class PrimeSieve(generator.Generator):
    def j_increment(self, j):
        return [int(math.pow(j, 2) + (n * j)) for n in
                itertools.takewhile(lambda x: int(math.pow(j, 2) + (x * j)) <= self.maximum, range(0, self.maximum))]

    def generate(self):
        logger.info("Starting prime generation")
        numbers = [True] * (self.maximum + 1)
        for i in range(2, int(math.sqrt(self.maximum))):
            if numbers[i]:
                for j in self.j_increment(i):
                    numbers[j] = False
        self.data = [i for i, j in enumerate(numbers) if j and i > 1]
