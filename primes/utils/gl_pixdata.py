from PIL import Image


"""Wrapper module for converting an OpenGL (vispy) canvas to an image."""
def pixels_to_image(pixels, size, path):
    """Reads an array of pixels (RGBA) and outputs a png image.
    
    Arguments:
        pixels -- Array of pixel data to read.
        size -- width and height of the image in a tuple.
        path -- A filepath to save the output image to.
    """
    img = Image.new("RGBA", size)
    pix = img.load()
    for y, row in enumerate(pixels):
        for x, col in enumerate(row):
            if y < size[1] and x < size[0]:
                pix[x, y] = tuple(col)
    img.save(path)
