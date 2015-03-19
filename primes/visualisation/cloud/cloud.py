from PIL import Image
import logging


logger = logging.getLogger(__name__)
class PrimeCloud():
    def __init__(self, generator, settings):
        self.settings = settings
        self.generator = generator(self.settings["min"], self.settings["max"])
        self.width = self.settings["width"]
        self.height = self.settings["height"]
        self.limit = self.settings["max"]
        self.current_x = int(self.width / 2)
        self.current_y = int(self.height / 2)
        #self.current_x = 0
        #self.current_y = 0
        self.output = []

    def bound_check(self):
        if self.current_x < 0:
            self.current_x = self.width - 1
        if self.current_x >= self.width:
            self.current_x = 0
        if self.current_y < 0:
            self.current_y = self.height - 1
        if self.current_y >= self.height:
            self.current_y = 0

    def next_point(self, x):
        if x == 1:
            self.current_y -= 1
        elif x == 2:
            self.current_y += 1
        elif x == 3:
            self.current_x += 1
        elif x == 4:
            self.current_x -= 1
        elif x == 5:
            self.current_y -= 1
        self.bound_check()

    def generate(self):
        for y in range(self.height):
            self.output.append([])
            for x in range(self.width):
                self.output[y].append(0)
        self.generator.generate()
        for counter in self.generator.data:
            # put the modulus in settings somewhere
            x = counter % 16
            self.next_point(x)
            self.output[self.current_y][self.current_x] += 1000000

    def to_image(self, imagename):
        self.generate()
        img = Image.new("RGBA", (self.width, self.height), self.settings["bgcolour"])
        pix = img.load()
        for i, y in enumerate(self.output):
            for j, x in enumerate(y):
                pix[i, j] = ((x >> 16) & 255, (x >> 8) & 255, x & 255, 255)
        img.save(imagename)
