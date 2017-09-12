import json
with open(r"D:/pyCharm/Aipingjsongetopentimefinish/AipinwanFood台南timeget.json") as f:
    x=json.load(f)
namelist=[]
for i in range(0,len(x)):
    try:
        if i > 0:
            if  x[i]["name"] in namelist:
                x.remove(x[i])
            else:
                namelist.append(x[i]["name"])
        else:
            namelist.append(x[i]["name"])
    except:
        pass
with open('D:\pyCharm\Aipingjsongetopentimefinish/TainanUnique.json', 'w') as f:
    json.dump(x, f)