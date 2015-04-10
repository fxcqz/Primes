from PIL import Image
import logging
import math
import primes.visualisation.generic as generic
from primes.visualisation.gl_base import Canvas


logger = logging.getLogger(__name__)
class SimpleGrid(generic.Generic):
    def __init__(self, generator, settings):
        super(self.__class__, self).__init__(generator, settings)
        self.output = []

    def generate(self):
        self.generator.generate()
        new_lim = int(math.ceil(self.limit ** 0.5))
        for elem in self.generator.data:
            x = int(elem % new_lim) - 1
            y = int(elem // new_lim)
            self.output.append((x, y))

    def to_gl(self, parent_):
        self.generate()
        canv = Canvas(keys='interactive', size=(640., 480.), resizable=False, limit=self.limit, \
            bgcolour=self.settings['bgcolour'], fgcolour=self.settings['colour'], parent=parent_)
        for p in self.output:
            canv.set_colour(self.settings['colour'], canv.grid, p)
        return canv
