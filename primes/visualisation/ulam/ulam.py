from PIL import Image
import logging


logger = logging.getLogger(__name__)
class UlamSpiral():
    def __init__(self, generator, settings):
        self.settings = settings
        self.generator = generator(self.settings["min"], self.settings["max"])
        self.width = self.settings["width"]
        self.height = self.settings["height"]
        #self.limit = self.width + (self.height * self.width)
        self.limit = self.settings["max"]
        self.current_x = int(self.width / 2)
        self.current_y = int(self.height / 2)
        self.delta = 1
        self.direction = 0
        self.counter = 1
        self.side = 1
        self.output = []

    def next_point(self):
        if self.direction == 0:
            self.current_y += 1
        if self.direction == 1:
            self.current_x -= 1
        if self.direction == 2:
            self.current_y -= 1
        if self.direction == 3:
            self.current_x += 1

    def generate(self):
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
        logger.info("generating image")
        self.generate()
        logger.info("writing to image")
        img = Image.new("RGBA", (self.width, self.height), self.settings["bgcolour"])
        pix = img.load()
        for p in self.output:
            if p[0] in range(0, self.width) and p[1] in range(0, self.height):
                pix[p[0], p[1]] = self.settings["colour"]
        img.save(imagename)
