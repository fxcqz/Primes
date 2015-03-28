class Generic(object):
    def __init__(self, generator, settings):
        self.settings = settings
        self.generator = generator(self.settings["min"], self.settings["max"])
        self.width = self.settings["width"]
        self.height = self.settings["height"]
        self.limit = self.settings["max"]

    def set_specifics(self, data):
        pass
