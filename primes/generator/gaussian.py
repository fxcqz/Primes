import numpy as np
import prime
import generator
import logging
import primes.utils.logger as log


log.setup_logging()
logger = logging.getLogger(__name__)

class Generator(generator.Generator):
    def __init__(self, minimum=0, maximum=1):
        super(self.__class__, self).__init__(minimum, maximum)
        self.path = "primes/generator/data/gaussians/"
        self.datatype = complex
        self.threshold = 300
        self.limit = max([np.real(self.minimum) ** 2 + np.imag(self.minimum) ** 2,
                          np.real(self.maximum) ** 2 + np.imag(self.maximum) ** 2])
        sieve = prime.Generator(maximum=int(self.limit))
        sieve.generate()
        self.primes = sieve.data

    def generate(self):
        logger.info("Checking cache")
        self.data = self.read_cache()
        cache_miss = self.not_in_cache()
        if self.data:
            if len(cache_miss[0]) + len(cache_miss[1]) < self.threshold:
                for n in cache_miss[0]:
                    if self.is_gaussian_prime(n):
                        self.data.insert(0, n)
                for n in cache_miss[1]:
                    if self.is_gaussian_prime(n):
                        self.data.append(n)
        else:
            gaussians = []
            logger.info("Starting generation")
            for i in range(np.real(self.minimum), np.real(self.maximum)):
                for j in range(np.imag(self.minimum), np.imag(self.maximum)):
                    z = np.complex(i, j)
                    if self.is_gaussian_prime(z):
                        gaussians.append(z)
                logger.info("%s", str(i))
            logger.info("Writing data")
            self.data = np.array(gaussians)

    def is_gaussian_prime(self, z):
        re = np.real(z)
        im = np.imag(z)
        result = False
        if re != 0 and im != 0 and re ** 2 + im ** 2 in self.primes:
            result = True
        elif re == 0 and abs(im) in self.primes and abs(im) % 4 == 3:
            result = True
        elif im == 0 and abs(re) in self.primes and abs(re) % 4 == 3:
            result = True
        return result
