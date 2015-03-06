import os
import logging
import primes.utils.logger as log
from primes.utils.custom_complex import CustomComplex
import numpy


# TODO:
# use cached data
log.setup_logging()
logger = logging.getLogger(__name__)

class Generator(object):
    def __init__(self, minimum=0, maximum=1):
        self.minimum = minimum
        self.maximum = maximum
        self.path = "primes/generator/data/"
        self.datatype = int
        # maximum number of elements missing from cache to do full generation
        self.threshold = 100
        self.data = None

    def generate(self):
        pass

    # cache read

    def data_files_from_dir(self):
        return filter(lambda x: ".dat" in x, list(os.walk(self.path))[0][2])

    def read_cache(self):
        files = self.data_files_from_dir()
        logger.info(files)
        data = None
        logger.info("Checking cache")
        for f_ in files:
            with open(self.path + f_, 'r') as f:
                data = numpy.loadtxt(f, delimiter=',', dtype=self.datatype)
                logger.info("Finding pertinent data (%s - %s)", self.minimum, self.maximum)
                data = filter(lambda x: self.minimum <= x <= self.maximum, data)
                logger.info("Data length %s", str(len(data)))
        if data:
            logger.info("Removing duplicates")
            data = list(set(data))
            logger.info("Sorting data")
            data.sort()
        else:
            logger.info("No data found in cache")
        return data

    def complex_range(self, minimum, maximum):
        zs = []
        for i in range(numpy.real(minimum), numpy.real(maximum)):
            for j in range(numpy.imag(minimum), numpy.imag(maximum)):
                zs.append(CustomComplex(i, j))
        return zs

    def not_in_cache(self):
        if self.datatype == complex:
            return filter(lambda x: CustomComplex(self.minimum) <= x < CustomComplex(self.data[0]),
                                    self.complex_range(self.minimum, self.data[0])), \
                   filter(lambda x: CustomComplex(self.data[-1]) < x <= CustomComplex(self.maximum),
                                    self.complex_range(self.data[-1], self.maximum))
        return filter(lambda x: self.minimum <= x < min(self.data), range(self.minimum, min(self.data))), \
               filter(lambda x: max(self.data) < x <= self.maximum, range(max(self.data), self.maximum + 1))

    # cache write

    def next_filename(self, path):
        try:
            if os.path.exists(os.path.dirname(path)):
                logger.info("Retrieving path info")
                _, _, files = os.walk(path).next()
                return str(len(files) + 1) + ".dat"
            else:
                logger.warning("No path available, creating one")
                os.makedirs(os.path.dirname(path))
        except StopIteration:
            pass
        return "1.dat"

    def to_file(self):
        if not self.data:
            self.generate()
        try:
            filename = self.next_filename(self.path)
            if not os.path.exists(os.path.dirname(self.path)):
                os.makedirs(os.path.dirname(self.path))
            with open(self.path + filename, 'w') as f:
                logger.info("Writing data to file %s", self.path + filename)
                f.write(','.join([str(n) for n in self.data]))
        except IOError:
            logger.error("Failed to write data", exc_info=True)
