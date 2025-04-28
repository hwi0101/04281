# reference: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

import os, glob
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                print("No EXIF geotagging found")
                return None

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def read_exif(in_dir, out_file):
    
    img_list = glob.glob("%s/*.jpg" % in_dir)
    
    num_img = len(img_list)
    
    if num_img == 0:
        print('找不到 JPG 影像檔!\n')
        return
    
    fout = open(out_file, 'w')
    header = '檔案名稱,拍攝時間,經度,緯度\n'
    fout.write(header)

    for i in range(num_img):
        basename = os.path.basename(img_list[i])
        #print(basename)
        img = Image.open(img_list[i])
        exif = img._getexif()

        labeled = get_labeled_exif(exif)
        time = labeled['DateTimeOriginal']
        
        geotags = get_geotagging(exif)
        
        if geotags == None:
            data = '{},{}\n'.format(basename, time)
        else:   
            lat, lon = get_coordinates(geotags)
            data = '{},{},{},{}\n'.format(basename, time, lon, lat)
        
        fout.write(data)
        
    fout.close()

in_dir = input('enter name of image folder: ')
out_file = input('enter output file name: ')

print('reading images from: ', in_dir)
read_exif(in_dir, out_file)

print('done')