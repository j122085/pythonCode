
def TF_IDF(contentlist):
    contentcutlist=[]
    import jieba
    jieba.set_dictionary(r'D:\WordLibrary\JiebaUse\jieba_dict.txt.big')
    stopwordset = set()
    with open(r'D:\WordLibrary\JiebaUse\stopwords.txt', 'r', encoding='utf-8') as sw:
        for line in sw:
            stopwordset.add(line.strip('\n'))
            
    for content in contentlist:
        words = jieba.cut(content, cut_all=False)
        cutcontent = " ".join([word for word in words if word not in stopwordset and '\u4e00' <= word <= '\u9fff'])

        contentcutlist.append(cutcontent)

    from collections import Counter
    wordCountlist = [Counter(contentcut.split(" ")).most_common(300) for contentcut in contentcutlist]
    TfList = [[((wordkv[0], wordkv[1] / sum(dict(wordCount).values()))) for wordkv in wordCount] for wordCount in wordCountlist]
    wordlist = []
    for wordCount in wordCountlist:
        for wordkv in wordCount:
            wordlist.append(wordkv[0])
    wordlist = set(wordlist)
    Ntext = len(contentlist)
    wordappear = {}
    for word in wordlist:
        n = 0
        for contentcut in contentcutlist:
            if word in contentcut:
                n += 1
        wordappear[word] = n
    import math
    IDFlist = {word: math.log(Ntext / wordappear[word], 10) for word in wordappear}
    TF_IDFlist = [Counter({wordkv[0]: wordkv[1] * IDFlist[wordkv[0]] for wordkv in Tf}) for Tf in TfList]
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



