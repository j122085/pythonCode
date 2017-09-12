##新版
import requests
from bs4 import BeautifulSoup as bs
import os
import json
import time
import re
from collections import OrderedDict

def getcommentlist(dienlist):
    commentlist = []
    for url in olddict["comment"]:
        if 'checkin' not in url:
            res = requests.get(url)
            print(url)
            print(res.status_code)
            try:
                if res.status_code == 200:
                    soup = bs(res.text, 'lxml')
                    res.close()
                    try:
                        opentime = re.findall("([0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]|[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]、[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05])",
                            soup.select('#shop-header > div.info > div.hours > div > span')[0].text)[0]
                    except:
                        try:
                            opentime = re.findall("([0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]|[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05]、[0-2][0-9]\:[0-6][05]\~[0-2][0-9]\:[0-6][05])",
                                soup.select('#shop-header > div.info > div.hours > p')[0].text)[0]
                        except:
                            opentime = None
                    title = soup.select("#comment > header > div > div > h1")[0].text.replace("\n", "").strip().replace(" ", "")
                    name = soup.select("#comment > header > div > figure > figcaption > h3 > a > span")[0].text
                    comment = "".join([i.text for i in soup.select('div.description')]).replace("\u200b", "").replace(
                        "\u3000", "").replace("\n", "").replace("\xa0", "").replace("\t", "").replace(" ", "")
                    date = soup.select('p.inline.date > span')[0].text
                    click = int(
                        soup.select("#comment > header > div > div > div.actions > span")[1].text.split("共 ")[1].split(
                            " 次瀏覽")[0].replace(",", ""))
                    push = int(soup.select("#good-push")[0].text)
                    try:
                        replys = [re.findall('.[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}([^檢舉]*)',
                                             reply.text.replace("\n", "").replace("\xa0", ""))[0] for reply in
                                  soup.select("#reply > li")]
                    # replys=[re.findall('.[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}(.+)檢*',reply.text.replace("\n","").replace("\xa0",""))[0].split("檢")[0] for reply in soup.select("#reply > li")]
                    except:
                        replys = None
                commentdict = OrderedDict()
                commentdict["url"] = url
                commentdict["name"] = name
                commentdict["date"] = date
                commentdict["title"] = title
                commentdict["content"] = comment
                commentdict["click"] = click
                commentdict["push"] = push
                commentdict["message"] = replys
                try:
                    commentdict['business_hours'] = opentime
                except:
                    pass
                commentlist.append(commentdict)
            except:
                pass
    return commentlist


for filename in os.listdir("./Aipingjson/"):
    with open("./Aipingjson/" + filename) as jf:
        jsonContent = json.load(jf)
        newlist = []
        count = 0
        for olddict in jsonContent:
            # time.sleep(5)
            count+=1
            if count%10==0:
                time.sleep(3)
            if count%30==0:
                if not os.path.exists('./Aipingjsonfinish'):
                    os.makedirs('./Aipingjsonfinish')
                with open('./Aipingjsonfinish/finish' + filename, 'w') as f:
                    json.dump(newlist, f)
            newdict = {}
            try:
                newCommentlist = getcommentlist(olddict)
                olddict["comment"] = newCommentlist
            except:
                pass
            newlist.append(olddict)

        if not os.path.exists('./Aipingjsonfinish'):
            os.makedirs('./Aipingjsonfinish')

        with open('./Aipingjsonfinish/finish' + filename, 'w') as f:
            json.dump(newlist, f)