#中枢程序
import tkinter as tk
import os
import iat_ws_python3 as iat
from gensim import corpora, models
import jieba.posseg as jp
import jieba
import BDBKPC as bd
import sys
import time
jieba.setLogLevel(jieba.logging.INFO)
def get_text(texts):
   flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 词性
   stopwords = ('sh','ch''zh','z','s','c','h','w','也','和','的', '就', '是', '用', '还', '在', '上', '作为','我','它','他','她','不')  # 停用词
   words_list = []
   for text in texts:
       words = [w.word for w in jp.cut(text) if w.flag in flags and w.word not in stopwords]
       words_list.append(words)
   if words_list == []:
      return "无结果"
   return words_list 
def LDA_model(words_list):
    dictionary = corpora.Dictionary(words_list)
    corpus = [dictionary.doc2bow(words) for words in words_list]
    lda_model = models.ldamodel.LdaModel(corpus=corpus, num_topics=2, id2word=dictionary, passes=10)
    return lda_model
def GetStart():
        while True:
                texts=['']
                #iat.main()
                p=open('fileout1.txt','r')
                word=get_text([p.read()])
                LDA_model(word)
                lda_model = LDA_model(word)
                word = lda_model.show_topic(0, 5)
                k=open("fileout2.txt","w")
                print("关键词如下")
                print("s=skip 1=word1 2=word2 3=word3 以此类推")
                for i in word:
                    texts.append(i)
                    if len(i[0])<=1:
                       word.remove(i)
                       continue
                    print(i[0])
                cmd=input()
                if cmd=='s':
                    continue
                try:
                      cmd=int(cmd)
                      k.write(word[cmd-1][0]+'\n')
                      k.write("break")
                      k.close()
                      #print(1)
                      bd.main()
                      #print(2)
                      result=[]
                      with open("outs.txt","r") as f:
                              for fli in f:
                                      result.append(str(fli.strip("").split(',')))
                                      #print("result->",result)
                      word=get_text(result)
                      LDA_model(word)
                      lda_model = LDA_model(word)
                      word = lda_model.show_topic(0, 5)
                      print("以下为该词语关键词:")
                      for i in word:
                         if len(i[0])<=1:
                            continue
                         print(i[0])
                      print("以下为完整释义")
                      for i in result:
                         if '（' in i:
                            aaa=i.index('（')
                            bbb=i.index('）')
                            print(aaa,bbb)
                            for r in range(aaa,bbb):
                               del i[r]
                         print(i[2:-4])
                      time.sleep(5)
                except:
                      print("无结果")
GetStart()
