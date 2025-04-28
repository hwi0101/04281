from PIL import Image
from PIL.ExifTags import TAGS

file_name = 'images/P_20171007_095928.jpg'
img = Image.open(file_name)
print(img)
exif = img._getexif()

if exif is not None:
    for (tag, value) in exif.items():
        print('tag = ', tag)
        print('value = ', value)
        key = TAGS.get(tag, tag)
        print(key + ' = ' + str(value))
