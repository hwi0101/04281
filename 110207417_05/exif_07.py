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

def read_exif(in_dir, out_file, kml_file):
    
    img_list = glob.glob("%s/*.jpg" % in_dir)
    
    num_img = len(img_list)
    
    if num_img == 0:
        print('找不到 JPG 影像檔!\n')
        return
    
    fout = open(out_file, 'w')
    header = '檔案名稱,拍攝時間,經度,緯度\n'
    fout.write(header)

    kml_out = open(kml_file, 'w')
    kml_out.write(kml_header)

    for i in range(num_img):
        basename = os.path.basename(img_list[i])
        print('reading exif from: ', basename)
        
        img = Image.open(img_list[i])
        width, height = img.size
        
        new_w = int(width / 10)
        new_h = int(height / 10)
        
        exif = img._getexif()

        labeled = get_labeled_exif(exif)
        time = labeled['DateTimeOriginal']
        
        geotags = get_geotagging(exif)
        
        if geotags == None:
            data = '{},{}\n'.format(basename, time)
        else:   
            lat, lon = get_coordinates(geotags)
            data = '{},{},{},{}\n'.format(basename, time, lon, lat)
            
            kml_out.write(place_mark.format(basename,basename,basename,new_w,new_h,lon,lat))
        
        fout.write(data)
        
    fout.close()
    
    kml_out.write(kml_trailer)
    kml_out.close()

kml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"  xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom ">
<Folder>
'''
place_mark = '''<Placemark>  
  <name>{}</name>  
  <description>{} 
    <p><img alt="" src="images/{}" width="{}" height="{}" /></p> 
    <p><a href="http://www.nccu.edu.tw/">http://www.nccu.edu.tw/</a></p>  
  </description> 
  <Point>  
    <coordinates>{},{},0</coordinates>  
  </Point>  
</Placemark>  
'''
kml_trailer = '''</Folder>
</kml>
'''

in_dir = input('enter name of image folder: ')
out_file = input('enter output CSV file name: ')
kml_file = input('enter output KML file name: ')

print('reading images from: ', in_dir)
read_exif(in_dir, out_file, kml_file)

print('done')