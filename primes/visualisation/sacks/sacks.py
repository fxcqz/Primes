__author__ = 'Matt'
from PIL import Image
import numpy as np
import logging
import primes.utils.coordinates as coordinates


logger = logging.getLogger(__name__)
class SacksSpiral():
    def __init__(self, generator, settings):
        self.settings = settings
        self.generator = generator(self.settings["min"], self.settings["max"])
        self.width = self.settings["width"]
        self.height = self.settings["height"]
        # TODO: maybe use pol to cart to determine width/height/limit
        self.limit = self.settings["max"]

    def to_image(self, imagename):
        self.generator.generate()
        img = Image.new("RGBA", (self.width, self.height), self.settings["bgcolour"])
        pix = img.load()
        for point in self.generator.data:
            coords = coordinates.pol_to_cart(np.sqrt(point), np.sqrt(point) * 2 * np.pi)
            # TODO: use circles instead of pixels
            pix[int(coords[0]) + self.width / 2, int(coords[1]) + self.height / 2] = \
                self.settings["colour"]
        img.save(imagename)
