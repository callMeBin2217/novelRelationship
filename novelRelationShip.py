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

import matplotlib
import wordcloud
import jieba


class novelRelationShip():
	def __init__(self):
		#读入小说和人物名单
		with open('names.txt','r',encoding='utf-8') as f :
			self.names = list(name.strip() for name in f.readlines())

		with open('novel.txt','r',encoding='utf-8') as f :
			self.content = list(n.strip() for n in f.readlines())


	def  
