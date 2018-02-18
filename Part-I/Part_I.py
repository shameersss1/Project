from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os,sys
from math import cos, asin, sqrt
import pandas as pd


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))*1000   #2*R*asin..


def get_field (exif) :
    res={}
    if exif:
      for (k,v) in exif.iteritems():
          if TAGS.get(k) == "GPSInfo":
              res[TAGS.get(k)]=v

    return res

data={'Time':[],'Images':[]}

with open("/home/shameer/Desktop/Skylarks/software_dev/videos/DJI_0301.SRT", "r+") as ins:
    array = []
    i=0
    for line in ins:
        array.append(line)

for i in range(0,len(array),4):
    time=array[i+1]
    loc =array[i+2].split(',')
    lat1=float(loc[1])
    logt1=float(loc[0])
    src=""





    for f in os.listdir("/home/shameer/Desktop/Skylarks/software_dev/images"):
            if f.endswith(".JPG"):
                file_name = f
                path = "/home/shameer/Desktop/Skylarks/software_dev/images/" + file_name
                img = Image.open(path)
                exif_data=img._getexif()
                res=get_field(exif_data)

                if "GPSInfo" in res:
                    lat = float(res["GPSInfo"][2][0][0]) + float(res["GPSInfo"][2][1][0]) / 60.00 + float(res["GPSInfo"][2][2][0]) / (3600.00 * float(res["GPSInfo"][2][2][1]))
                    lon = float(res["GPSInfo"][4][0][0]) + float(res["GPSInfo"][4][1][0]) / 60.00 + float(res["GPSInfo"][4][2][0]) / (3600.00 * float(res["GPSInfo"][4][2][1]))
                    
                    if res["GPSInfo"][1] !="N":
                        lat=lat*-1
                    
                    if res["GPSInfo"][3] !="E":
                        lon=lon*-1
                    
                    if distance(lat1, logt1, lat, lon) <= 35.00:
                        src = src + f + ", "
                        
                   



    if(len(src)>0):
        data['Time'].append(time)
        data["Images"].append(src)
        print(time + ": " + src)




df = pd.DataFrame(data, columns = ['Time', 'Images'])
df.to_csv('/home/shameer/Desktop/example.csv')















