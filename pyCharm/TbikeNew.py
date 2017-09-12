import time
import requests
import pprint
import json
count = 0
d = 1
tbikelist = []
while True:
    res = requests.get("http://tbike.tainan.gov.tw:8081/Service/StationStatus/Json")
    count += 1
    tbikelist.append(res.json())
    if count % 1440 == 0:
        d = d + 1
        tbikelist = []
    if count % 5 == 0:
        print(str(time.ctime()))
        with open("D:/Data/JsonData/Tbike/" + str(time.ctime().replace(" ", "_").replace(":", "-"))[:10] + "-" + str(
                d) + ".json", "w") as f:
            json.dump(tbikelist, f)
    time.sleep(60)
