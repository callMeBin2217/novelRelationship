__author__='callMeBin'
#-*-encoding:utf-8-*-

'''
用python分析 小说斗破苍穹里的人物关系
准备：
	1、novel.txt(斗破苍穹小说)
	2、names.txt(人物名单)
	3、stopwords.txt(常用中文停用词)
	4、matplotlib(用来展示图)
	5、wordcloud(生成词云)
'''

import matplotlib.pyplot as plt
from pylab import mpl
from wordcloud import WordCloud
import jieba
import pandas as pd
from pandas import DataFrame
import jieba.analyse
import gensim

class novelRelationShip():
	def __init__(self):
		#读入小说和人物名单、中文停用词
		with open(r'D:/gitHub/novelRelationship/names.txt','r',encoding='utf-8') as f :
			self.names = list(name.strip() for name in f.readlines())

		with open(r'D:/gitHub/novelRelationship/novel.txt','r',encoding='utf-8') as f :
			self.content = list(n.strip() for n in f.readlines())

		with open(r'D:/gitHub/novelRelationship/stopwords.txt','r',encoding='utf-8') as f:
			self.STOPWORDS = [word.strip() for word in f.readlines()]


	#统计人物列表中出场的次数
	def findPeopleCount(self,num=10):
		novel = ''.join(self.content)
		counts = []
		for name in self.names:
			counts.append([name,novel.count(name)])

		counts.sort(key=lambda v : v[1],reverse=True)

		return counts[:num]


	#制作DataFrame
	def showAsDataFrame(self,data):
		show = DataFrame(data,columns=['names','counts'])
		return show

	#制作频率直方图
	def showAsMat(self,show):
		#设置中文字体
		mpl.rcParams['font.sans-serif']=['SimHei']
		data = list(show.counts)
		index = list(show.names)
		plt.bar(range(len(data)),data,tick_label=index)
		plt.xlabel(r'出现的人物')
		plt.ylabel(r'出现的次数')
		plt.title(r'斗破苍穹人物出现频次图')
		plt.savefig(r'D:/gitHub/novelRelationship/img.jpg')


	#找出文中关键词和制作词云
	def showAsWordCloud(self):
		print(r'正在分析小说关键词:')

		tags = jieba.analyse.extract_tags(' '.join(self.content),topK=20,withWeight=True)
		for k,v in tags :
			 print('关键词:{},     权重:{:.3f}'.format(k,v))

		txt = ''.join([v+',' for v,x in tags])
		wc = WordCloud(background_color='white',font_path='simhei.ttf',max_font_size=40).generate(txt)
		plt.imshow(wc)
		plt.axis('off')
		plt.show()
		wc.to_file(r'D:/gitHub/novelRelationship/wc.jpg')
		return tags

	#分词和训练模型
	def getModel(self,tags):
		for tag,x in tags:
			jieba.add_word(tag)
		for name in self.names:
			jieba.add_word(name)
		print(r'开始分词....')
		sentence =[]
		for line in self.content:
			seg_list = list(jieba.cut(line,cut_all=False))
			unique_list =[]
			for seg in seg_list:
				if seg not in self.STOPWORDS:
					unique_list.append(seg)
			sentence.append(unique_list)
		print(r'分词结束...开始训练...')
		model = gensim.models.Word2Vec(sentence,size=100,window=5,min_count=4,workers=4)
		print(r'训练模型完毕并保存模型')
		model.save(r'D:/gitHub/novelRelationship/dbcq.model')


	#模型分析测试
	def modelText(self):
		model = gensim.models.Word2Vec.load(r'D:/gitHub/novelRelationship/dbcq.model')
		
		print(r'==============和萧炎类似的人物=========')
		for s in model.most_similar(positive=['萧炎'])[:5]:
			print(s)
		print('\n\n')


		print(r'==============女主角=========')
		for s in model.most_similar(positive=['薰儿']):
			print(s)
		print('\n\n')

		print(r'============药老的徒弟============')
		pupil = model.most_similar(positive=['韩枫','萧炎'],negative=['药尘'],topn=1)
		print(pupil)







a = novelRelationShip()
#print(a.findPeopleCount())
#count = a.findPeopleCount()
#show = a.showAsDataFrame(count)
#a.showAsMat(show)
#print(show)
#tags = a.showAsWordCloud()
#a.getModel(tags)
a.modelText()
