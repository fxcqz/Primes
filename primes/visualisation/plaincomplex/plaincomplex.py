from PIL import Image
import logging


logger = logging.getLogger(__name__)
class PlainComplex():
    def __init__(self, generator, settings):
        self.settings = settings
        self.generator = generator(self.settings["min"], self.settings["max"])
        self.width = self.settings["width"]
        self.height = self.settings["height"]
        self.limit = self.settings["max"]

    def to_image(self, imagename):
        self.generator.generate()
        img = Image.new("RGBA", (self.width, self.height), self.settings["bgcolour"])
        pix = img.load()
        for y in range(-(int(self.height / 2)), int(self.height / 2)):
            for x in range(-(int(self.width / 2)), int(self.width / 2)):
                if complex(x, y) in self.generator.data:
                    pix[x+int(self.width/2), y+int(self.height/2)] = self.settings["colour"]
        img.save(imagename)
