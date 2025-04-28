# reference: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

from PIL import Image

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

img_name = 'images/IMG_20191019_134659.jpg'
exif = get_exif(img_name)
print(exif)