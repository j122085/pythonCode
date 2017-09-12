import jieba
import logging
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# jieba custom setting.
jieba.set_dictionary('D:/WordLibrary/JiebaUse/jieba_dict.txt.big')

# load stopwords set
stopwordset = set()
with open('D:/WordLibrary/JiebaUse/stopwords.txt','r',encoding='utf-8') as sw:
    for line in sw:
        stopwordset.add(line.strip('\n'))
#---------------------------------------------------------------------------台南小吃名詞
with open("D:/Data/JsonData/TainanFood/TainanUniqueXY.json",encoding='utf-8') as f:
    contentss=json.load(f)
Dienlist=[i["name"] for i in contentss]
stylelist=[i["style"] for i in contentss]
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
#---------------------------------------------------------------------------

output = open('D:\Data\word2VecData\TainanContent.txt','w',encoding="utf-8")

texts_num = 0

for dien in contentss:
    for comment in dien['comment']:
        content=comment["content"]
        words = jieba.cut(content, cut_all=False)
        for word in words:
            if word not in stopwordset and '\u4e00' <= word and word <= '\u9fff':
                output.write(word +' ')
        texts_num += 1
        if texts_num % 1000 == 0:
            logging.info("已完成前 %d 篇的斷詞" % texts_num)
output.close()


from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus("D:/Data/word2VecData/TainanContent.txt")

model = word2vec.Word2Vec(sentences, size=300,window=6, min_count=4, workers=4,sg=1)
# sentences:當然了，這是要訓練的句子集，沒有他就不用跑了
# size:這表示的是訓練出的詞向量會有幾維
# alpha:機器學習中的學習率，這東西會逐漸收斂到 min_alpha
# sg:這個不是三言兩語能說完的，sg=1表示採用skip-gram,sg=0 表示採用cbow
# window:還記得孔乙己的例子嗎？能往左往右看幾個字的意思
# workers:執行緒數目，除非電腦不錯，不然建議別超過 4
# min_count:若這個詞出現的次數小於min_count，那他就不會被視為訓練對象

# Save our model.
model.save("D:/Data/word2VecData/Tainan.model.bin")
