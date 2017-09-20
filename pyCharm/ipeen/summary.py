import pymongo
import re
import json
import jieba
from collections import Counter
import time
import math
import gc

startt=time.time()

#登入pymongo
clinet=pymongo.MongoClient("mongodb://10.120.27.23:27017/")
db=clinet['rawData']
ipeenjson=list(db.Tainan_final.find({}))

# 結巴 匯入自己的詞典
jieba.set_dictionary('D:/WordLibrary/JiebaUse/jieba_dict.txt.big')

# 停止詞字典stopwordset
stopwordset = set()
with open('D:/WordLibrary/JiebaUse/stopwords.txt', 'r', encoding='utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))

# 店家名稱字典dienlist
dienlist = [dien["name"] for dien in ipeenjson]

# 店家種類字典stylelist
stylelist = [dien["style"] for dien in ipeenjson]

# 店家種類字典introductionlist
introductionlist = [dien["introduction"] for dien in ipeenjson]

# 店家種類字典coordinatelist
coordinatelist = [dien['coordinate'] for dien in ipeenjson]

# 自製餐廳相關字字典pinlist
with open("D:\Data\csvtest\MyDict.csv") as f:
    mydict = f.read()
# linewords pindict每個字的評分dict
linewords = [{myword: float(line.split(",")[0]) for myword in line.split(",")[1:]} \
             for line in mydict.split("\n") if line.split(",")[0] != ""]
pindict = {}
for word in linewords:
    pindict.update(word)
pinlist = list(pindict.keys())

# 將以上字典都加入斷詞行列
for i in dienlist:
    jieba.add_word(i)
for i in stylelist:
    jieba.add_word(i)
for i in pinlist:
    if i != "":
        jieba.add_word(i)

# 店家評論總數Ncommentlist
Ncommentlist = [len(i["comment"]) for i in ipeenjson]

#各店家評論diencommentlist
diencommentlist=[[j["content"] for j in i["comment"]] for i in ipeenjson]

#各店家回覆dienmessagelist
dienmessagelist=[[''.join(j["message"]) for j in i["comment"] if j["message"]!=None and j["message"]!='null'] for i in ipeenjson]

#回覆數量Nmessagelist
Nmessagelist=[len(dienmessage) for dienmessage in dienmessagelist]

#全部回覆+全部評論
dienallpinlist=[diencomment+dienmessage for diencomment,dienmessage in zip(diencommentlist,dienmessagelist)]

#把所有回覆合併
messagecombinlist=[" ".join(["".join(meg) for meg in megs if meg!=None and meg!='null'and meg!='']) for megs in dienmessagelist]

#把所有評論合併
commentcombinelist = [" ".join([j["content"] for j in i["comment"]]) for i in ipeenjson]

#合併評論+回覆
pincombinelist=[comment+" "+message for comment,message in zip(commentcombinelist,messagecombinlist)]

#清一下記憶體
gc.collect()

st = time.time()
# 取得各店家的斷完詞評論pincutlist
pincutlist = []
cutcount = 0
for pincombine in pincombinelist:
    cutcount += 1
    if cutcount % 200 == 0:
        print("以切" + str(cutcount) + "篇文章的詞")
    words = jieba.cut(pincombine, cut_all=False)
    pincut = " ".join([word for word in words if word not in stopwordset and
                       '\u4e00' <= word and word <= '\u9fff'])  # and word not in dienlist and word not in pinlist
    pincutlist.append(pincut)

# 所有店家的用詞加總前三百wordCountlist300
wordCountlist = [Counter(pincut.split(" ")).most_common(300) for pincut in pincutlist]

# TF計算 (TF=這個字出現的次數/這篇文章的總字數)
# (sum(dict(wordCount).values())=>一篇所有字的字數  wordkv[1]>>該文字字數  wordkv[0]>>該文字)
# TFList每篇文章的詞 的詞頻
TFList = [[((wordkv[0], wordkv[1] / sum(dict(wordCount).values()))) for wordkv in wordCount] for wordCount in
          wordCountlist]

# 全文章共用了幾個詞(set可以去除重複，可迭代)
wordlist = []
for wordCount in wordCountlist:
    for word in wordCount:
        wordlist.append(word[0])
wordlist = set(wordlist)

# nDien所有的文章(店家)數
ndien = len(dienlist)

# wordappear計算每個字出現於 (幾篇) 文章
wordappear = {}
appearcount = 0
for word in wordlist:
    appearcount += 1
    if appearcount % 1000 == 0:
        print("以計算" + str(appearcount) + "個文字的出現篇數")
    n = 0
    for pincut in pincutlist:
        if word in pincut:
            n += 1
    wordappear[word] = n

# IDF(逆向檔案頻率)=某詞  所有文章數/在幾篇文章出現 開log10 >>次方數為所
IDFlist = {word: math.log(ndien / wordappear[word], 10) for word in wordappear}

# dienTF每家店的全字TF值 wordTF每個詞的TF   wordTF[0]詞 wordTF[1]詞的TF值  IDFlist[wordTF[0]]詞的IDF值
TF_IDFlist = [Counter({wordTF[0]: wordTF[1] * IDFlist[wordTF[0]] for wordTF in dienTF}) for dienTF in TFList]
for name, TFIDF in zip(dienlist, TF_IDFlist):
    if name in TFIDF:
        del TFIDF[name]

et = time.time()
print(et - st)

gc.collect()

#pinCountMaxper5list 一個店家出現的餐廳相關詞數量(一個篇評論的相同詞最多給5個分數)
st=time.time()
pinCountMaxper5list = []
countN=0
for dienallpin in dienallpinlist:
    dienWordcount={}
    for allpin in  dienallpin:
        countN+=1
        if countN%100==0:
            print("已算完"+str(countN)+"篇情緒字")
        for pinword in pinlist:
            if len(re.findall(pinword,allpin))>0:
                if len(re.findall(pinword,allpin))>5:
                    npinword=5
                else:
                    npinword=len(re.findall(pinword,allpin))
                if pinword not in dienWordcount:
                    dienWordcount[pinword]=0
                dienWordcount[pinword]+=npinword
    pinCountMaxper5list.append(dienWordcount)
ed=time.time()
print(ed-st)

#將六篇回覆視為一篇文章，做正規化(防止評論數過多的店家分數極端化)
Npartpin=[int(Nmessage/6)+Ncomment for Nmessage,Ncomment in zip(Nmessagelist,Ncommentlist)]


#大致計算每家店的分數dienscorelist
dienscorelist=[]
for pinCount,N in zip(pinCountMaxper5list,Npartpin):
    dienscore=0
    for pin in pinCount:
        dienscore+=pinCount[pin]*pindict[pin]/N
    dienscorelist.append(dienscore)

#mydict為自己的字典的資料
#格式為:
######否開頭tag 為 非否tag 反義
#給予正分數 tag評價詞(非否評價) 同意字群同意字群同意字群同意字群同意字群同意字群
#給予負分數 tag評價詞(否開頭評價) 同意字群同意字群同意字群同意字群同意字群同意字群
#給予正分數 tag評價詞(非否評價) 同意字群同意字群同意字群同意字群同意字群同意字群
#給予負分數 tag評價詞(否開頭評價) 同意字群同意字群同意字群同意字群同意字群同意字群

#line.split(",")[1]為tag!!! word為與tag對應的同義字
synonyms=[{word:line.split(",")[1] for word in line.split(",")[1:]} for line in mydict.split("\n") if line.split(",")[0]!=""]

pinsynonymsdict={}
for synonym in synonyms:
    pinsynonymsdict.update(synonym)
del pinsynonymsdict[""]

# 取得各餐廳的評價特徵分數featurescores!!!
featurescores = []

# 將評價詞加總及評論次數做iterate
for pinCountMaxper5, N in zip(pinCountMaxper5list, Npartpin):
    dienfeaturescore = {}

    # 評價詞出現次數/評論次數 做為分數，其中否字開頭給負分
    for pin in pinCountMaxper5:
        if pin != "":
            if pinsynonymsdict[pin][0] == "否":
                if pinsynonymsdict[pin][1:] not in dienfeaturescore:
                    dienfeaturescore[pinsynonymsdict[pin][1:]] = 0
                dienfeaturescore[pinsynonymsdict[pin][1:]] -= round(pinCountMaxper5[pin] / N, 2) * 1
            else:
                if pinsynonymsdict[pin] not in dienfeaturescore:
                    dienfeaturescore[pinsynonymsdict[pin]] = 0
                dienfeaturescore[pinsynonymsdict[pin]] += round(pinCountMaxper5[pin] / N, 2)
    if len(dienfeaturescore) == 0:
        dienfeaturescore["無評"] = 1
    featurescores.append(dienfeaturescore)

BigAnalyzeTable = []
for name, style, Ncomment, contentcut, wordCount, TFIDF, pinCountMax5, score, featurescore, introduction, coordinate in zip(
        dienlist, stylelist, Npartpin, pincutlist, wordCountlist, TF_IDFlist, pinCountMaxper5list, dienscorelist,
        featurescores, introductionlist, coordinatelist):
    dien = {}
    dien['name'] = name
    dien['style'] = style
    dien['Ncomment'] = Ncomment
    dien['contentcut'] = contentcut
    dien['wordCount'] = wordCount
    dien['TF_IDF'] = TFIDF
    dien['pinCountMaxper5'] = pinCountMax5
    dien['score'] = score
    dien['featurescores'] = featurescore
    dien['tags'] = [tag[0] for tag in Counter(TFIDF).most_common(5)]

    dien['introduction'] = introduction
    dien['coordinate'] = coordinate

    BigAnalyzeTable.append(dien)

gc.collect()

#算出每個評論的評論數N時的 最大值b 最小值g for正規化


#allpin=評論詞list
allpin=set([line.split(",")[1] for line in mydict.split("\n") if line.split(",")[0]!="" and line.split(",")[1][0]!="否"])
standard={}

#standard為正規化所需用的值
for pin in allpin:
    for rang in [(0,5),(5,10),(10,15),(15,100)]:
        get={}
        values=[dien['featurescores'][pin] for dien in BigAnalyzeTable if pin in dien['featurescores'] and dien["Ncomment"]>rang[0] and dien["Ncomment"]<=rang[1]]
        b=0
        g=0
        for value in values:
            if value <b:
                b=round(value,1)
            if value >g:
                g=round(value,1)
        get[pin+str(rang[0])]=((g+b)/2,g-(g+b)/2)
        standard.update(get)


#進行正規化的處理
for dien in BigAnalyzeTable:
    N=dien['Ncomment']
    for feature in dien['featurescores']:
        if feature !="無評":
            if N<6:
                dien['featurescores'][feature]=round((dien['featurescores'][feature])/standard[feature+str(0)][1],2)
            elif N<11 and N>=6:
                dien['featurescores'][feature]=round((dien['featurescores'][feature])/standard[feature+str(5)][1],2)
            elif N<16 and N>=11:
                dien['featurescores'][feature]=round((dien['featurescores'][feature])/standard[feature+str(10)][1],2)
            else:
                dien['featurescores'][feature]=round((dien['featurescores'][feature])/standard[feature+str(15)][1],2)

pipin=[('食物美味','食物不好吃',"非常好吃",'非常不好吃'),('划算','價格較高昂',"非常便宜",'非常貴')
       ,('環境好','環境比較不好',"環境超棒",'環境很差'),('服務好','服務較差',"服務一級棒",'服務很差')
       ,('其他正面情緒','評論有些負面情緒詞',"網路評論正面情緒非常多",'網路評論負面情緒很多')]
moods=[mood[0] for mood in pipin]
for dien in BigAnalyzeTable:
    newtag=[]
    for feature in dien["featurescores"]:
        if feature in moods:
            if dien["featurescores"][feature]>1:
                for pinpare in pipin:
                    if feature==pinpare[0]:
                        newtag.append(pinpare[2])
            elif dien["featurescores"][feature]>0.4:
                newtag.append(feature)
            elif dien["featurescores"][feature]<-0.5:
                for pinpare in pipin:
                    if feature==pinpare[0]:
                        newtag.append(pinpare[3])
            elif dien["featurescores"][feature]<0.0:
                for pinpare in pipin:
                    if feature==pinpare[0]:
                        newtag.append(pinpare[1])
        else:
            if dien["featurescores"][feature]>0.7:
                newtag.append(feature)

gooddien=[i for i in BigAnalyzeTable if i['score']>30 and i['Ncomment']>10]



with open('D:/Data/JsonData/TainanFood/_bigtable_1.3.json','w') as f:
    json.dump(BigAnalyzeTable,f)
with open('D:/Data/JsonData/TainanFood/_TainanGoodDien_1.1.json','w') as f:
    json.dump(gooddien,f)

endd=time.time()

print(startt-endd)