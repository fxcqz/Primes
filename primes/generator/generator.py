import os
import logging
import primes.utils.logger as log
from primes.utils.custom_complex import CustomComplex
import numpy


#log.setup_logging()
logger = logging.getLogger(__name__)

class Generator(object):
    def __init__(self, minimum=0, maximum=1):
        self.minimum = minimum
        self.maximum = maximum
        self.path = "primes/generator/data/"
        self.datatype = int
        # maximum number of elements missing from cache to do full generation
        self.threshold = 100
        self.data = []

    def generate(self):
        pass

    def get_data(self):
        return self.data

    # cache read
    # TODO: optimise by not reading redundant data

    def data_files_from_dir(self):
        return filter(lambda x: ".dat" in x, list(os.walk(self.path))[0][2])

    def read_cache(self):
        if os.path.exists(os.path.dirname(self.path)):
            files = self.data_files_from_dir()
            logger.info(files)
            data = None
            tdata = []
            logger.info("Checking cache")
            if any(files):
                for f_ in files:
                    with open(self.path + f_, 'r') as f:
                        data = numpy.loadtxt(f, delimiter=',', dtype=self.datatype)
                        logger.info("Finding pertinent data (%s - %s)", self.minimum, self.maximum)
                        tdata += list(data)
                        logger.info("Data length %s", str(len(data)))
            if tdata:
                logger.info("Removing duplicates")
                tdata = list(set(tdata))
                tdata = filter(lambda x: self.minimum <= x <= self.maximum, tdata)
                logger.info("Sorting data")
                tdata.sort()
            else:
                logger.info("No data found in cache")
            return numpy.array(tdata)
        return []

    def complex_range(self, minimum, maximum):
        zs = []
        for i in range(numpy.real(minimum), numpy.real(maximum)):
            for j in range(numpy.imag(minimum), numpy.imag(maximum)):
                zs.append(CustomComplex(i, j))
        return zs

    #def not_in_cache(self):
    #    if self.datatype == complex:
    #        return filter(lambda x: CustomComplex(self.minimum) <= x < CustomComplex(self.data[0]),
    #                                self.complex_range(self.minimum, self.data[0])), \
    #               filter(lambda x: CustomComplex(self.data[-1]) < x <= CustomComplex(self.maximum),
    #                                self.complex_range(self.data[-1], self.maximum))
    #    return filter(lambda x: self.minimum <= x < min(self.data), range(self.minimum, min(self.data))), \
    #           filter(lambda x: max(self.data) < x <= self.maximum, range(max(self.data), self.maximum + 1))
    def not_in_cache(self):
        ret = None
        if len(self.data) != 0:
            if self.datatype == complex:
                ret = self.complex_range(self.minimum, self.data[0]), \
                       self.complex_range(self.data[-1] + complex(1, 1), 
                                          self.maximum + complex(1, 1))
            else:
                ret = range(self.minimum, min(self.data)), \
                      range(max(self.data) + 1, self.maximum + 1)
        if ret:
            if len(ret[0]) + len(ret[1]) > self.threshold:
                ret = None
        return ret

    # cache write
    # TODO: this can be improved to not cache duplicate data
    #       (file rotation/size cap etc)

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
        if not any(self.data):
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
