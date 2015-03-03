import numpy as np
import prime
import generator


class GaussianPrime(generator.Generator):
    def __init__(self, path, minimum=0, maximum=1):
        super(self.__class__, self).__init__(path, minimum, maximum)
        self.limit = max([np.real(self.minimum) ** 2 + np.imag(self.minimum) ** 2,
                          np.real(self.maximum) ** 2 + np.imag(self.maximum) ** 2])
        sieve = prime.PrimeSieve("primes/generator/data/primes/",
                                 maximum=self.limit)
        sieve.generate()
        self.primes = sieve.data

    def generate_gaussian_primes(self):
        gaussians = []
        for i in range(np.real(self.minimum), np.real(self.maximum)):
            for j in range(np.imag(self.minimum), np.imag(self.maximum)):
                z = np.complex(i, j)
                if self.is_gaussian_prime(z):
                    gaussians.append(z)
        self.data = gaussians

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
