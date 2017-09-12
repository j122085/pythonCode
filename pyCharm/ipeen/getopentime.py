from bs4 import BeautifulSoup as bs
import time
import requests
import os
import json
import re
for filename in os.listdir('./Aiping/'):
    if not os.path.exists('./Aipingjson/' + filename.split(".")[0] + '.json'):
        with open('./Aiping/' + filename, encoding='utf-8') as data:
            x = data.read()
            urls = x.split(",")
            count = 0
            biglist = []
            for url in urls:
                url = url.split("-")[0]
                res = requests.get(url)
                if res.status_code == 200:
                    count += 1
                    print(count)
                    if count % 50 == 0:
                        time.sleep(3)
                    if count % 50 == 0:
                        if not os.path.exists('Aipingopentime'):
                            os.makedirs('Aipingopentime')
                        with open('./Aipingopentime/' + filename.split(".")[0] + 'opentime.json', 'w') as f:
                            json.dump(biglist, f)
                    soup = bs(res.text, 'lxml')
                    res.close

                    #     print(soup.select("#shop-header > div.info > h1 > span")[0].text.strip())
                    #     print(soup.select("#shop-header > div.info > div.brief > p.cate.i > a")[0].text)
                    #     print(soup.select("#shop-header > div.info > div.brief > p.tel.i > a")[0].text.replace("-",""))
                    #     print(soup.select("#shop-header > div.info > div.brief > p.addr.i > a")[0].text.strip())
                    #     print(soup.select("#shop-header > div.info > div.brief > p.cost.i")[0].text.strip().split("  ")[1].split(" ")[0])
                    #     print(soup.select("#shop-summary > div.summary")[0].text.strip().replace(" ",""))
                    #     print(soup.select("#shop-header > div.info > div.hours")[0].text)
                    #     print(soup.select("#shop-header > div.info > div.hours > div > span"))

                    peenlist = []
                    dien = {}
                    try:
                        opentime = re.findall("([0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]|[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]、[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05])",
                            soup.select('#shop-header > div.info > div.hours > div > span')[0].text)[0]
                    except:
                        try:
                            opentime = re.findall("([0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]|[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]、[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05])",
                                soup.select('#shop-header > div.info > div.hours > p')[0].text)[0]
                        except:
                            opentime = None
                    try:
                        dien['name'] = soup.select("#shop-header > div.info > h1 > span")[0].text.strip()
                        dien['business_hours'] = opentime
                        print(dien)
                        biglist.append(dien)
                    except:
                        pass
            # print(peenlist)
            if not os.path.exists('Aipingjsonopentime'):
                os.makedirs('Aipingjsonopentime')
            with open('./Aipingjsonopentime/' + filename.split(".")[0] + 'opentime.json', 'w') as f:
                json.dump(biglist, f)