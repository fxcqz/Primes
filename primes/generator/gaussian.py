# -*- coding: utf-8 -*-
import numpy as np
import prime
import generator
import logging


logger = logging.getLogger(__name__)

class Generator(generator.Generator):
    """Generator child class for generating Gaussian Primes.

    Note that minimum and maximum inputs to this class have type of complex,
    rather than the usual int.

    Attributes:
        limit (int): The limit  required to  generate the  list of  primes. This
                     needs to  be  calculated to  fully  cover  the range of the 
                     gaussian primes.
        primes (list): Set of primes required to  construct the list of gaussian
                       primes.
    
    Keyword Arguments:
        minimum -- the lower limit of the dataset (default complex(0, 0))
        maximum -- the upper limit of the dataset (default complex(1, 1))
    """
    def __init__(self, minimum=complex(0, 0), maximum=complex(1, 1)):
        super(self.__class__, self).__init__(minimum, maximum)
        self.path = "primes/generator/data/gaussians/"
        self.datatype = complex
        # the threshold for this dataset should be slightly more lenient 
        # than usual
        self.threshold = 300
        self.limit = max([np.real(self.minimum)**2 + np.imag(self.minimum)**2,
                          np.real(self.maximum)**2 + np.imag(self.maximum)**2])
        sieve = prime.Generator(maximum=int(self.limit))
        sieve.generate()
        self.primes = sieve.data

    def generate(self):
        """Generates the set  of Gaussian Primes within  the constraints  of the 
        minimum and maximum passed to this class, subject to values outputted by
        the `is_gaussian_prime' function.
        
        See the  generate  function stub  in the Generator parent class for more
        information.
        """
        logger.info("Checking cache")
        self.data = self.read_cache()
        cache_miss = self.not_in_cache()
        if cache_miss:
            self.data = list(self.data)
            for n in cache_miss[0]:
                if self.is_gaussian_prime(n):
                    self.data.insert(0, n)
            for n in cache_miss[1]:
                if self.is_gaussian_prime(n):
                    self.data.append(n)
            self.data = np.array(self.data)
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
            self.to_file()

    def is_gaussian_prime(self, z):
        """Function  to  determine  whether  the  imputed  complex  number is  a
        Gaussian Prime, subject to the following constraints.

        Let z be expressed as a complex number in the form: z = a + bi;  where a
        is the real component and b is the imaginary component. A Gaussian Prime
        therefore is complex number where ONE of the following is true:
            1) If both a and b are nonzero then, a + bi is a  Gaussian Prime iff
               a**2 + b**2 is an ordinary prime.
            2) If a = 0, then bi is a  Gaussian Prime  iff abs(b) is an ordinary
               prime and abs(b) % 4 = 3.
            3) If b = 0, then a  is a  Gaussian Prime  iff abs(a) is an ordinary
               prime and abs(a) % 4 = 3.

        Arguments:
            z -- a complex number
        """
        if not isinstance(z, complex):
            return False
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
