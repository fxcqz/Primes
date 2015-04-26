from PIL import Image
import logging
import math
import primes.visualisation.generic as generic
from primes.visualisation.gl_base import Canvas


logger = logging.getLogger(__name__)
class UlamSpiral(generic.Generic):
    """For visualising data on the Ulam Spiral.

    Attributes:
        current_x -- the current x position of the pointer.
        current_y -- the current y position of the pointer.
        delta -- the current length of the side within the spiral based on the
                 pointers location.
        direction -- the current direction the pointer is moving in.
        counter -- the current value corresponding to the pointer.
        side -- tracks how many sides have been covered (delta increases by one
                for each time side changes twice).
        output -- output array of the generation.
    """
    def __init__(self, generator, settings):
        super(self.__class__, self).__init__(generator, settings)
        self.current_x = int(self.width / 2)
        self.current_y = int(self.height / 2)
        self.delta = 1
        self.direction = 0
        self.counter = 1
        self.side = 1
        self.output = []

    def next_point(self):
        """Determines the next location of the pointer based on the current
        direction.
        """
        if self.direction == 0:
            self.current_y += 1
        if self.direction == 1:
            self.current_x -= 1
        if self.direction == 2:
            self.current_y -= 1
        if self.direction == 3:
            self.current_x += 1

    def generate(self):
        """See primes.visualisation.generic for more information."""
        logger.info("generating data")
        self.generator.generate()
        logger.info("starting ulam")
        while self.counter <= self.limit:
            for k in range(self.delta):
                if self.counter in self.generator.data:
                    self.output.append([self.current_x, self.current_y, self.counter])
                self.counter += 1
                self.next_point()
            if self.side % 2 == 0:
                self.delta += 1
            self.direction = (self.direction + 1) % 4
            self.side += 1

    def to_image(self, imagename):
        """See primes.visualisation.generic for more information."""
        logger.info("generating image")
        self.generate()
        logger.info("writing to image")
        img = Image.new("RGBA", (self.width, self.height), self.settings["bgcolour"])
        pix = img.load()
        for p in self.output:
            if p[0] in range(0, self.width) and p[1] in range(0, self.height):
                pix[p[0], p[1]] = self.settings["colour"]
        img.save(imagename)

    def to_gl(self, parent_):
        """See primes.visualisation.generic for more information."""
        new_lim = int(math.ceil(self.limit ** 0.5))
        self.current_x = (new_lim**2/new_lim)/2
        self.current_y = (new_lim**2/new_lim)/2
        self.generate()
        canv = Canvas(keys='interactive', size=(637., 437.), resizable=False, limit=self.limit,
            bgcolour=self.settings['bgcolour'], fgcolour=self.settings['colour'], parent=parent_,
            data=self.output)
        return canv
