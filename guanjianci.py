from gensim import corpora, models
import jieba.posseg as jp
import jieba
class textan:
    def __init__(self):
        pass
    def get_text(self,texts):
        flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 词性
        stopwords = ('的', '就', '是', '用', '还', '在', '上', '作为','我','它','他','她','不')  # 停用词
        words_list = []
        for text in texts:
            words = [w.word for w in jp.cut(text) if w.flag in flags and w.word not in stopwords]
            words_list.append(words)
        return words_list

    def LDA_model(self,words_list):
        # 构造词典
        # Dictionary()方法遍历所有的文本，为每个不重复的单词分配一个单独的整数ID，同时收集该单词出现次数以及相关的统计信息
        dictionary = corpora.Dictionary(words_list)
        #print(dictionary)
        #print('打印查看每个单词的id:')
        #print(dictionary.token2id)  # 打印查看每个单词的id
     
        # 将dictionary转化为一个词袋
        # doc2bow()方法将dictionary转化为一个词袋。得到的结果corpus是一个向量的列表，向量的个数就是文档数。
        # 在每个文档向量中都包含一系列元组,元组的形式是（单词 ID，词频）
        corpus = [dictionary.doc2bow(words) for words in words_list]
        #print('输出每个文档的向量:')
        #print(corpus)  # 输出每个文档的向量
     
        # LDA主题模型
        # num_topics -- 必须，要生成的主题个数。
        # id2word    -- 必须，LdaModel类要求我们之前的dictionary把id都映射成为字符串。
        # passes     -- 可选，模型遍历语料库的次数。遍历的次数越多，模型越精确。但是对于非常大的语料库，遍历太多次会花费很长的时间。
        lda_model = models.ldamodel.LdaModel(corpus=corpus, num_topics=2, id2word=dictionary, passes=10)
     
        return lda_model
    def starter(self):
        p=open("fileout1.txt","r")
        word=self.get_text([p.read()])
        self.LDA_model(word)
        lda_model = self.LDA_model(word)
        word = lda_model.show_topic(0, 5)
        k=open("fileout2.txt","w")
        for i in word:
            k.write(i[0]+'\n')
        k.close()
#d=textan()
#print('ok')
#d.starter()
#print('ok')
