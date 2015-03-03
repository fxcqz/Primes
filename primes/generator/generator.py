import os
import logging
import primes.utils.logger as log


# TODO:
# use cached data
log.setup_logging()
logger = logging.getLogger(__name__)

class Generator():
    def __init__(self, path, minimum=0, maximum=1):
        self.minimum = minimum
        self.maximum = maximum
        self.path = path
        self.data = None

    def generate(self):
        pass

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
