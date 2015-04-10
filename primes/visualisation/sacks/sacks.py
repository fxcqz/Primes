__author__ = 'Matt'
from PIL import Image
import numpy as np
import logging
import primes.utils.coordinates as coordinates
import primes.visualisation.generic as generic
from primes.visualisation.gl_base import Canvas


logger = logging.getLogger(__name__)
class SacksSpiral(generic.Generic):
    def __init__(self, generator, settings):
        super(self.__class__, self).__init__(generator, settings)
        # TODO: maybe use pol to cart to determine width/height/limit

    def to_image(self, imagename):
        self.generator.generate()
        img = Image.new("RGBA", (self.width, self.height), self.settings["bgcolour"])
        pix = img.load()
        for point in self.generator.data:
            coords = coordinates.pol_to_cart(np.sqrt(point), np.sqrt(point) * 2 * np.pi)
            # TODO: use circles instead of pixels
            x = int(coords[0]) + self.width / 2
            y = int(coords[1]) + self.height / 2
            if 0 <= x < self.width and 0 <= y < self.height:
                pix[x, y] = self.settings["colour"]
        img.save(imagename)

    def to_gl(self, parent_):
        self.generator.generate()
        new_lim = int(np.ceil(self.limit ** 0.5))
        canv = Canvas(keys='interactive', size=(637., 437.), resizable=False, \
            limit=self.limit*4, bgcolour=self.settings['bgcolour'], fgcolour=self.settings['colour'], \
            parent=parent_)
        for point in self.generator.data:
            coords = coordinates.pol_to_cart(np.sqrt(point), np.sqrt(point) * 2 * np.pi)
            x = new_lim + int(coords[0])
            y = new_lim + int(coords[1])
            if 0 <= x < new_lim*2 and 0 <= y < new_lim*2:
                canv.set_colour(self.settings['colour'], canv.grid, (x, y))
        return canv
