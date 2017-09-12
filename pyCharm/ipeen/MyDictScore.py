with open("D:\Data\csvtest\MyDict.csv") as f:
    csv=f.read()
x=[i.split(",")[1:] for i in csv.split("\n") if i.split(",")[0]!=""]
pins=[]


for i in x:
    for j in i:
        pins.append(j)
x="\n".join(pins)
with open("D:\Data\csvtest\pinjia.txt","w") as pin:
    y=pin.write(x)

with open("D:\Data\csvtest\pinjia.txt") as pin:
    y=pin.read()
pins=y.split("\n")

with open("D:\WordLibrary\JiebaUse\stopwords.txt",encoding="utf8") as stopp:
    stop=stopp.read()
stopwords=stop.split("\n")

import json
with open("D:\Data\JsonData\TainanFood\TainanUniqueXY.json") as f:
    data=json.load(f)
names=[i["name"] for i in data]
styles=[i["style"] for i in data]

import jieba
jieba.set_dictionary("D:\WordLibrary\JiebaUse\jieba_dict.txt.big")
for i in pins:
    if i !="":
        jieba.add_word(i)
for i in names:
    jieba.add_word(i)
for i in styles:
    jieba.add_word(i)

#以上把jiebadict加入該斷的文字


x=[[j["content"] for j in i["comment"]] for i in data]
N=[len(i) for i in x]
contents=["  ".join(i) for i in x]


contentscut=[]
for i in contents:
    words=jieba.cut(i)
    contentcut=" ".join([word for word in words if word not in stopwords and '\u4e00' <= word <= '\u9fff'])
    contentscut.append(contentcut)
##對評論執行斷詞

analyzetable=[]
for name,style,n,contentcut in zip(names,styles,N,contentscut):
    dictt={}
    dictt["name"]=name
    dictt["style"]=style
    dictt["n"]=n
    dictt["contentcut"]=contentcut
    analyzetable.append(dictt)
#存取斷玩詞的物件
import json
with open("D:\Data\JsonData\TainanFood\AnalyzeTable2.json","w") as pin:
    json.dump(analyzetable,pin)

import json
with open("D:\Data\JsonData\TainanFood\AnalyzeTable2.json") as pin:
    analyzetable=json.load(pin)

with open("D:\Data\csvtest\MyDict.csv") as f:
    csv=f.read()
# x=[(float(i.split(",")[0]),i.split(",")[1:]) for i in csv.split("\n") if i.split(",")[0]!=""]
x=[{j:float(i.split(",")[0]) for j in i.split(",")[1:]} for i in csv.split("\n") if i.split(",")[0]!=""]


import pandas
from collections import Counter
for i in analyzetable:
    i["WordCount"]=Counter(i["contentcut"].split(" "))

pindict={}
for i in x:
    pindict.update(i)

#每家廠商
for dien in analyzetable:
    pinprice=0
    for word in dien["WordCount"]:
        if word in pindict:
            pinprice+=dien["WordCount"][word]*pindict[word]
    if dien['n']!=0:
        if dien['n']<6:
            dien["price"]=round((pinprice/dien["n"])*0.4,2)
        elif dien['n']<11:
            dien["price"]=round((pinprice/dien["n"])*0.6,2)
        elif dien['n']<16:
            dien["price"]=round((pinprice/dien["n"])*0.8,2)
        else:
            dien["price"]=round((pinprice/dien["n"])*1,2)

import json
with open("D:\Data\JsonData\TainanFood\MyDictPrice.json","w") as pin:
    json.dump(analyzetable,pin)