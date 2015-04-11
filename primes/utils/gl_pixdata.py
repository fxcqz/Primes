from PIL import Image


def pixels_to_image(pixels, size, path):
    img = Image.new("RGBA", size)
    pix = img.load()
    for y, row in enumerate(pixels):
        for x, col in enumerate(row):
            if y < size[1] and x < size[0]:
                pix[x, y] = tuple(col)
    img.save(path)
