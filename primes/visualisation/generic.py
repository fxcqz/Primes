class Generic(object):
    """Base class for visualisations.

    Sets up instance  variables which are  prevalent across all  visualisations,
    and also  implements a stub  for `set_specifics',  which is used by some but
    not all visualisations.

    Attributes:
        settings -- Dict holding all the settings for the visualisation.
        generator -- handle to the generator being used by the visualisation.
        width -- width of the visualisation.
        height -- height of the visualisation.
        limit -- upper limit in the dataset being used.

    Arguments:
        generator -- maps to the generator attribute.
        settings -- maps to the settings attribute.
    """
    def __init__(self, generator, settings):
        self.settings = settings
        self.generator = generator(self.settings["min"], self.settings["max"])
        self.width = self.settings["width"]
        self.height = self.settings["height"]
        self.limit = self.settings["max"]

    def set_specifics(self, data):
        """(Stub) Some visualisations  required additional or different settings
        to function  correctly. This function is used to set these values before
        running the visualisation.

        Arguments:
            data -- values which will map to unique instance variables on a per-
                    visualisation basis.
        """
        pass

    def generate(self):
        """(Stub) Formats the data taken from the generator in a unique way to
        be displayed as a visualisation.
        """
        pass

    def to_image(self, imagename):
        """(Stub) Saves the visualisation as an image."""
        pass

    def to_gl(self, parent_):
        """(Stub) Outputs the visualisation data on an OpenGL Canvas."""
        pass
