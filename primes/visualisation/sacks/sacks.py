__author__ = 'Matt'
from PIL import Image
import numpy as np
import logging
import primes.utils.coordinates as coordinates
import primes.visualisation.generic as generic


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
