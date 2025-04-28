# reference: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

img_name = 'images/IMG_20191019_134659.jpg'
exif = get_exif(img_name)
labeled = get_labeled_exif(exif)
print(labeled)