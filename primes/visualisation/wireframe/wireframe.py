import primes.visualisation.generic as generic
from gl_wireframe import Canvas


class Wireframe(generic.Generic):
    def __init__(self, generator, settings):
        super(self.__class__, self).__init__(generator, settings)

    def to_gl(self, parent_):
        self.generator.generate()
        canv = Canvas(keys='interactive', size=(637., 437.), resizable=False,
            limit=self.limit, bgcolour=self.settings['bgcolour'],
            fgcolour=self.settings['colour'], data=self.generator.data,
            parent=parent_)
        return canv
