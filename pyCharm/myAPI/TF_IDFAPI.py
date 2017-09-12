
def chinesetextcuting(text):
    print("如果有其他詞要斷，請先import jieba用jieba.add_word('要斷的詞')")
    import jieba
    jieba.set_dictionary('D:/pyCharm/dict.txt.big')
    stopwordset = set()
    with open('D:/pyCharm/stopwords.txt', 'r', encoding='utf-8') as sw:
        for line in sw:
            stopwordset.add(line.strip('\n'))
    words = jieba.cut(text, cut_all=False)
    cuttext = ""
    for word in words:
        if word not in stopwordset and '\u4e00' <= word <= '\u9fff':
            cuttext += word + " "
    return cuttext

def TF_IDF(textlist):
    textcutlist=[]
    import jieba
    jieba.set_dictionary('D:/pyCharm/dict.txt.big')
    stopwordset = set()
    with open('D:/pyCharm/stopwords.txt', 'r', encoding='utf-8') as sw:
        for line in sw:
            stopwordset.add(line.strip('\n'))
    for text in textlist:
        words = jieba.cut(text, cut_all=False)
        cuttext = ""
        for word in words:
            if word not in stopwordset and '\u4e00' <= word <= '\u9fff':
                cuttext += word + " "

        textcutlist.append(cuttext)

    from collections import Counter
    wordCountlist = [Counter(i.split(" ")).most_common(300) for i in textcutlist]
    TfList = [[((j[0], j[1] / sum(dict(i).values()))) for j in i] for i in wordCountlist]
    wordlist = []
    for i in wordCountlist:
        for j in i:
            wordlist.append(j[0])
    wordlist = set(wordlist)
    Ntext = len(textlist)
    wordappear = {}
    for i in wordlist:
        n = 0
        for j in textcutlist:
            if i in j:
                n += 1
        wordappear[i] = n
    import math
    IDFlist = {i: math.log(Ntext / wordappear[i], 10) for i in wordappear}
    TF_IDFlist = [Counter({j[0]: j[1] * IDFlist[j[0]] for j in i}) for i in TfList]
    return TF_IDFlist
# import os
import pprint
# ptttextlist=[]
# for dname in os.listdir("D:/jupyter/ptt_tou/"):
#     with open('D:/jupyter/ptt_tou/'+dname,encoding='utf-8') as f:
#         a=f.read()
#         ptttextlist.append(a)
# pttTF_IDF=TF_IDF(ptttextlist)
# pprint.pprint(pttTF_IDF[:5])
aaa=["你是一個白癡白癡白癡白癡智障加三級跳喜憨兒炫砲","dasgdasgds你還是去洗洗洗洗洗洗洗洗睡吧，腦殘 炫砲?","你你你你你你洗洗洗洗洗洗這個天才無敵炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲炫砲腦殘"]

x=TF_IDF(aaa)
pprint.pprint(x)



