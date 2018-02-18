from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os,sys
from math import cos, asin, sqrt
import pandas as pd


def get_field (exif) :
    res={}
    if exif:
      for (k,v) in exif.iteritems():
          if TAGS.get(k) == "GPSInfo":
              res[TAGS.get(k)]=v
        
    return res
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))*1000   #2*R*asin..


data = pd.read_csv('/home/shameer/Desktop/Skylarks/software_dev/assets.csv')

for i in range(0,len(data)):
    lat1 = float(data["latitude"][i])
    logt1= float(data["longitude"][i])

    src=""

    for f in os.listdir("/home/shameer/Desktop/Skylarks/software_dev/images"):
        if f.endswith(".JPG"):
            file_name = f
            path = "/home/shameer/Desktop/Skylarks/software_dev/images/" + file_name
            img = Image.open(path)
            exif_data=img._getexif()
            res=get_field(exif_data)
            
            if "GPSInfo" in res:
                lat = float(res["GPSInfo"][2][0][0]) + float(res["GPSInfo"][2][1][0])/60.00 + float(res["GPSInfo"][2][2][0])/(3600.00*float(res["GPSInfo"][2][2][1]))
                lon = float(res["GPSInfo"][4][0][0]) + float(res["GPSInfo"][4][1][0])/60.00 + float(res["GPSInfo"][4][2][0])/(3600.00*float(res["GPSInfo"][4][2][1]))
                
                if distance(lat1,logt1,lat,lon) <=50.00 :
                    src=src+f+", "
                

                
    if(len(src)>0):
        data["image_names"][i]=src



data.to_csv('/home/shameer/Desktop/example.csv')
