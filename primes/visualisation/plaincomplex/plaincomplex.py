from PIL import Image
import numpy as np
import logging
import primes.visualisation.generic as generic
from primes.visualisation.gl_base import Canvas


logger = logging.getLogger(__name__)
class PlainComplex(generic.Generic):
    """For simply displaying complex numbers on complex coordinates.
    
    Note:
        This visualisation is made unique by the dataset it uses rather than the
        visualisation itself.

    See primes.visualisation.generic for more information.
    """
    def __init__(self, generator, settings):
        super(self.__class__, self).__init__(generator, settings)

    def to_image(self, imagename):
        """See primes.visualisation.generic for more information."""
        self.generator.generate()
        img = Image.new("RGBA", (self.width, self.height), self.settings["bgcolour"])
        pix = img.load()
        for y in range(-(int(self.height / 2)), int(self.height / 2)):
            for x in range(-(int(self.width / 2)), int(self.width / 2)):
                if complex(x, y) in self.generator.data:
                    pix[x+int(self.width/2), y+int(self.height/2)] = self.settings["colour"]
        img.save(imagename)

    def to_gl(self, parent_):
        """See primes.visualisation.generic for more information."""
        self.generator.generate()
        min_ = self.settings['min']
        max_ = self.settings['max']
        new_lim = int(max([abs(np.real(min_)) + abs(np.real(max_)),
                       abs(np.imag(min_)) + abs(np.imag(max_))]))
        canv = Canvas(keys='interactive', size=(637., 437.), resizable=False, \
            limit=new_lim**2, bgcolour=self.settings['bgcolour'], \
            fgcolour=self.settings['colour'], parent=parent_)
        try:
            for y in range(int(np.imag(min_)), int(np.imag(max_))):
                for x in range(int(np.real(min_)), int(np.real(max_))):
                    if complex(x, y) in self.generator.data:
                        canv.set_colour(self.settings['colour'], canv.grid, (((new_lim/2)+x), ((new_lim/2)+y)))
        except IndexError:
            pass
        return canv
