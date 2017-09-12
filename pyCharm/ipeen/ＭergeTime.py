import requests
from bs4 import BeautifulSoup as bs
import os
import json
import time
import re
# jsonContent=[]
# timeContent=[]
from collections import OrderedDict

with open("D:/pyCharm/Aipingjsonfinish/finishAipinwanFood台南.json") as jf:
    jsoncontent = json.load(jf)

with open("D:/pyCharm/Aipingopentime/AipinwanFood台南opentime.json") as tf:
    timecontent = json.load(tf)
for i in jsoncontent:
    for j in timecontent:
        if i['name'] == j['name']:
            i['business_hours'] = j['business_hours']
print(jsoncontent[6010])
with open('./Aipingjsonopentime/AipinwanFood台南' + 'timeget.json', 'w') as f:
    json.dump(jsoncontent, f)