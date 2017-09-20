import json
import pprint
import re
import jieba
from collections import Counter
import time


st=time.time()
jieba.set_dictionary('D:/WordLibrary/JiebaUse/jieba_dict.txt.big')
stopwordset = set()
with open('D:/WordLibrary/JiebaUse/stopwords.txt', 'r', encoding='utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))
# ---------------------------------------------------------------------------台南小吃名詞
with open("D:\Data\JsonData\TainanFood\TainanUniqueXY.json") as f:
    contentss = json.load(f)
Dienlist = [i["name"] for i in contentss]
stylelist = [i["style"] for i in contentss]

#---------------------------------------------------------------------------原創字典詞
with open("D:\Data\csvtest\MyDict.csv") as f:
    csv=f.read()
x=[{j:float(i.split(",")[0]) for j in i.split(",")[1:]} for i in csv.split("\n") if i.split(",")[0]!=""]
pindict={}
for i in x:
    pindict.update(i)
pinlist=list(pindict.keys())

#---------------------------------------------------------------------------將相關字詞全加入結巴字典
for i in Dienlist:
    jieba.add_word(i)
for i in stylelist:
    jieba.add_word(i)
for i in pinlist:
    if i !="":
        jieba.add_word(i)




with open("D:\Data\JsonData\TainanFood\TainanUniqueXY.json") as f:
    allcontent = json.load(f)
# 取得店名
Dienlist = [i["name"] for i in allcontent]
# 取得總類
stylelist = [i["style"] for i in allcontent]
# 取得每家店的評論數
Ncomments = [len(i["comment"]) for i in allcontent]
# 取得每家店斷完詞的評論
contentcuts = []
comments = [" ".join([j["content"] for j in i["comment"]]) for i in allcontent]
# for content in comments:
#     words = jieba.cut(content, cut_all=False)
#     x = ""
#     for word in words:
#         if word not in stopwordset and '\u4e00' <= word and word <= '\u9fff':
#             x += word + " "
#     contentcuts.append(x)
cutcount=0
for content in comments:
    cutcount+=1
    if cutcount%200==0:
        print("以切"+str(cutcount)+"篇文章的詞")
    words = jieba.cut(content, cut_all=False)
    x=" ".join([word for word in words if word not in stopwordset and '\u4e00' <= word and word <= '\u9fff'])
    contentcuts.append(x)


contentcuts[0]



# Dienlist店名
# stylelist總類
# contentcuts斷詞評論
# Ncomments評論數
from collections import Counter
wordCountlist=[Counter(i.split(" ")).most_common(300) for i in contentcuts]
#wordCountlist所有店家的用詞加總前三百

Nword=[sum(dict(i).values()) for i in wordCountlist]
TfList=[[((j[0],j[1]/sum(dict(i).values()))) for j in i] for i in wordCountlist]
#TfList每篇文章詞頻

#IDF(逆向檔案頻率)=某詞  在幾篇文章出現/所有文章數 開log10 >>次方數為所需
import itertools
wordlist=[]
for i in wordCountlist:
    for j in i:
        wordlist.append(j[0])
wordlist=set(wordlist)
#wordlist所有的詞
nDien=len(Dienlist)
#nDien所有的文章數
wordappear={}
idfcount=0
for i in wordlist:
    idfcount+=1
    if idfcount%1000==0:
        print("以計算"+str(idfcount)+"個文字的出現篇數")
    n=0
    for j in contentcuts:
        if i in j:
            n+=1
    wordappear[i]=n
#wordappear每個字出現於 (幾篇) 文章
import math
IDFlist={i:math.log(nDien/wordappear[i],10) for i in wordappear}
#IDFlist每個字的 逆向檔案頻率
#TF-IDF=TF*IDF一篇文章的代表詞
# for i in TfList:
#     for j in i:
#         print(j)
TF_IDFlist=[Counter({j[0]:j[1]*IDFlist[j[0]]for j in i})for i in TfList]
#TF_IDFlist 每家店每個詞的TF-IDF
TF_IDFsortlist=[i.most_common(300) for i in TF_IDFlist]
#TF_IDFsortlist TF-IDF排序版
# Dienlist店名
# stylelist總類
# contentcuts斷詞評論
# Ncomments評論數
# wordCountlist所有店家的用詞加總前三百
# TfList每篇文章詞頻
# IDFlist每個字的 逆向檔案頻率
# wordlist所有的詞
# TF_IDFlist 每家店每個詞的TF-IDF
# TF_IDFsortlist TF-IDF排序版
import json
from collections import OrderedDict

AnalyzeTable = []
for name, style, Ncomment, wordCount, TF_IDF, contentcut in zip(Dienlist, stylelist, Ncomments, wordCountlist,
                                                                TF_IDFsortlist, contentcuts):
    diendict = {}
    diendict["name"] = name
    diendict["style"] = style
    diendict["Ncomment"] = Ncomment
    diendict["wordCount"] = dict(wordCount)
    diendict["TF_IDF"] = dict(TF_IDF)
    diendict["contentcut"] = contentcut
    AnalyzeTable.append(diendict)

with open('D:/Data/JsonData/TainanFood/TFIDFTable.json', 'w') as f:
    json.dump(AnalyzeTable, f)

et=time.time()

print(et-st)
