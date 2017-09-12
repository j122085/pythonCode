import googlemaps
import json

with open("D:\Data\JsonData\TainanFood\TainanUnique.json") as f:
    data = json.load(f)

import time

n = 0
gmaps = googlemaps.Client(key='AIzaSyAF9GKxqgmgDEW_h7M4TtM5CbkK03xnS0E')
for i in data:
    n += 1
    if i['coordinate'] == None:
        try:
            geocode_result = gmaps.geocode(i['address'])
            i['coordinate'] = geocode_result[0]['geometry']['location']
            time.sleep(1)
            print(i['address'])
            print(geocode_result[0]['geometry']['location'])
        except:
            pass
        if n % 10 == 0:
            with open("D:\Data\JsonData\TainanFood\TainanUnique.json", 'w') as f:
                json.dump(data, f)
with open("D:\Data\JsonData\TainanFood\TainanUnique.json", 'w') as f:
    json.dump(data, f)
data[4000]['coordinate']
