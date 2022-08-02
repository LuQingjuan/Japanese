import re
import os
import sys
import subprocess

TanngoFile = "Tanngo.md"
ResultFile = "Result.md"

HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっ"
KATAGANA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッーィェ"
Pseudonym = HIRAGANA + KATAGANA
FiftyToneDiagram = [["あ","い","う","え","お"],
					["か","き","く","け","こ"],
					["さ","し","す","せ","そ"],
					["た","ち","つ","て","と"],
					["な","に","ぬ","ね","の"],
					["は","ひ","ふ","へ","ほ"],
					["ま","み","む","め","も"],
					["ら","り","る","れ","ろ"],
					["が","ぎ","ぐ","げ","ご"],
					["ざ","じ","ず","ぜ","ぞ"],
					["だ","ぢ","づ","で","ど"],
					["ば","び","ぶ","べ","ぼ"],
					["ぱ","ぴ","ぷ","ぺ","ぽ"]]
DiagramDict = {"う":0, "く":1, "す":2, "つ":3, "ぬ":4, "ふ":5, "む":6, "る":7, "ぐ":8, "ず":9, "づ":10, "ぶ":11, "ぷ":12}
VTypeNameList = ["原形", "ます形", "て形", "た形", "意志形", "命令形", "假定形", "可能态", "被动态", "未然形", "使役态", "使役被动态", "禁止形", "ず形"]
ITypeNameList = ["原形", "です", "て形", "た形", "未然形", "副词化", "连体形", "假定形"]
NaTypeNameList = ["原形", "です", "て形", "た形", "未然形", "副词化", "连体形", "假定形"]
NTypeNameList = ["原形", "です", "て形", "た形", "未然形", "副词化", "连体形", "假定形"]
ATypeNameList = ["原形"]

class Comm_Word():
	def __init__(self):
		self.Word = ""
		self.Len = 0
		self.TypeNameList = []
		self.TypeFormatList = []
		self.WordStyleList = []
		self.WordStyleChangeLen = 0
	# V
	def GetTypeNameList(self):
		return self.TypeNameList

	# V
	def GetTypeFormatList(self):
		return self.TypeFormatList

	def GetWordStyleList(self):
		return self.WordStyleList

	def GetWordStyleChangeLen(self):
		return self.WordStyleChangeLen

class V_Word(Comm_Word):
	def __init__(self, Word):
		super(V_Word, self).__init__()
		self.TypeNameList = VTypeNameList
		self.Word = Word
		self.Len = len(Word)

	def SetV5TypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)
		# ます形 「う」->「い」
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][1] + "ます")
		# て形 た形
		if "う" == self.Word[-1] or "つ" == self.Word[-1] or "る" == self.Word[-1]:
			self.TypeFormatList.append(self.Word[:-1] + "って")
			self.TypeFormatList.append(self.Word[:-1] + "った")
		elif "む" == self.Word[-1] or "ぶ" == self.Word[-1] or "ぬ" == self.Word[-1]:
			self.TypeFormatList.append(self.Word[:-1] + "んで")
			self.TypeFormatList.append(self.Word[:-1] + "んだ")
		elif "く" == self.Word[-1]:
			if "行く" == self.Word:
				self.TypeFormatList.append(self.Word[:-1] + "って")
				self.TypeFormatList.append(self.Word[:-1] + "った")
			else:
				self.TypeFormatList.append(self.Word[:-1] + "いて")
				self.TypeFormatList.append(self.Word[:-1] + "いた")
		elif "ぐ" == self.Word[-1]:
			self.TypeFormatList.append(self.Word[:-1] + "いで")
			self.TypeFormatList.append(self.Word[:-1] + "いだ")
		elif "す" == self.Word[-1]:
			self.TypeFormatList.append(self.Word[:-1] + "して")
			self.TypeFormatList.append(self.Word[:-1] + "した")
		# 意志形 「う」->「お」
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][4] + "う")
		# 命令形 「う」->「え」
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][3])
		# 假定形 「う」->「え」
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][3] + "ば")
		# 可能态 「う」->「え」
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][3] + "る")
		if "う" == self.Word[-1]:
			# 被动态
			self.TypeFormatList.append(self.Word[:-1] + "わ" + "れる")
			# 未然形
			self.TypeFormatList.append(self.Word[:-1] + "わ" + "ない")
			# 使役态
			self.TypeFormatList.append(self.Word[:-1] + "わ" + "せる")
			# 使役被动态
			self.TypeFormatList.append(self.Word[:-1] + "わ" + "される")
			# 禁止形
			self.TypeFormatList.append(self.Word + "な")
			# ず形
			self.TypeFormatList.append(self.Word[:-1] + "わ" + "ず")
		else:
			# 被动态 「う」->「あ」
			self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][0] + "れる")
			# 未然形 「う」->「あ」
			if "ある" == self.Word:
				self.TypeFormatList.append("ない")
			else:
				self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][0] + "ない")
			# 使役态 「う」->「あ」
			self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][0] + "せる")
			# 使役被动态 「う」->「あ」
			if "す" == self.Word[-1]:
				self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][0] + "せられる")
			else:
				self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][0] + "される")
			# 禁止形
			self.TypeFormatList.append(self.Word + "な")
			# ず形 「う」->「あ」
			self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][0] + "ず")

	def SetV1TypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)
		# ます形
		self.TypeFormatList.append(self.Word[:-1] + "ます")
		# て形
		self.TypeFormatList.append(self.Word[:-1] + "て")
		# た形
		self.TypeFormatList.append(self.Word[:-1] + "た")
		# 意志形
		self.TypeFormatList.append(self.Word[:-1] + "よう")
		# 命令形
		self.TypeFormatList.append(self.Word[:-1] + "ろ")
		# 假定形
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][3] + "ば")
		# 可能态
		self.TypeFormatList.append(self.Word[:-1] + "られる")
		# 被动态
		self.TypeFormatList.append(self.Word[:-1] + "られる")
		# 未然形
		self.TypeFormatList.append(self.Word[:-1] + "ない")
		# 使役态
		self.TypeFormatList.append(self.Word[:-1] + "させる")
		# 使役被动态
		self.TypeFormatList.append(self.Word[:-1] + "させられる")
		# 禁止形
		self.TypeFormatList.append(self.Word + "な")
		# ず形
		self.TypeFormatList.append(self.Word[:-1] + "ず")

	def SetKaTypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)
		# ます形
		self.TypeFormatList.append(self.Word[:-2] + "きます")
		# て形
		self.TypeFormatList.append(self.Word[:-2] + "きて")
		# た形
		self.TypeFormatList.append(self.Word[:-2] + "きた")
		# 意志形
		self.TypeFormatList.append(self.Word[:-2] + "こよう")
		# 命令形
		self.TypeFormatList.append(self.Word[:-2] + "こい")
		# 假定形
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][3] + "ば")
		# 可能态
		self.TypeFormatList.append(self.Word[:-2] + "こられる")
		# 被动态
		self.TypeFormatList.append(self.Word[:-2] + "こられる")
		# 未然形
		self.TypeFormatList.append(self.Word[:-2] + "こない")
		# 使役态
		self.TypeFormatList.append(self.Word[:-2] + "こさせる")
		# 使役被动态
		self.TypeFormatList.append(self.Word[:-2] + "こさせられる")
		# 禁止形
		self.TypeFormatList.append(self.Word + "な")
		# ず形
		self.TypeFormatList.append(self.Word[:-2] + "こず")

	def SetSaTypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)
		# ます形
		self.TypeFormatList.append(self.Word[:-2] + "します")
		# て形
		self.TypeFormatList.append(self.Word[:-2] + "して")
		# た形
		self.TypeFormatList.append(self.Word[:-2] + "した")
		# 意志形
		self.TypeFormatList.append(self.Word[:-2] + "しよう")
		# 命令形
		self.TypeFormatList.append(self.Word[:-2] + "しろ・" + self.Word[:-2] + "せよ")
		# 假定形
		self.TypeFormatList.append(self.Word[:-1] + FiftyToneDiagram[DiagramDict[self.Word[-1]]][3] + "ば")
		# 可能态
		self.TypeFormatList.append(self.Word[:-2] + "できる")
		# 被动态
		self.TypeFormatList.append(self.Word[:-2] + "される")
		# 未然形
		self.TypeFormatList.append(self.Word[:-2] + "しない")
		# 使役态
		self.TypeFormatList.append(self.Word[:-2] + "させる")
		# 使役被动态
		self.TypeFormatList.append(self.Word[:-2] + "させられる")
		# 禁止形
		self.TypeFormatList.append(self.Word + "な")
		# ず形
		self.TypeFormatList.append(self.Word[:-2] + "せず")

	def SetTypeFormatList(self):
		if "する" == self.Word[-2:]:
			# "サ变"
			self.SetSaTypeFormatList()
			self.WordStyleChangeLen = 2
		elif "くる" == self.Word[-2:]:
			# "カ变"
			self.SetKaTypeFormatList()
			self.WordStyleChangeLen = 2
		elif "来る" == self.Word[-2:]:
			# "カ变"
			self.SetKaTypeFormatList()
			self.WordStyleChangeLen = 1
		elif "る" == self.Word[-1] and self.Word[-2] in "いえきけしせちてにねひへみめりれぎげじぜぢでびべぴぺ":
			# "一段"
			self.SetV1TypeFormatList()
			self.WordStyleChangeLen = 1
		else:
			#"知る","要る","入る","煎る","炒る","蹴る","減る","散る","練る","照る","切る","混じる","区切る","千切る","裏切る"]
			# "五段"
			self.SetV5TypeFormatList()
			self.WordStyleChangeLen = 1

	def SetWordStyleList(self):
		if 0 == len(self.TypeFormatList):
			self.SetTypeFormatList()
		# 原形
		self.WordStyleList.append(self.TypeFormatList[0])
		# ます形
		# ます　ません　ましょう　ました　ませんでした　まして
		self.WordStyleList.append(self.TypeFormatList[1][:-1])
		# て形
		self.WordStyleList.append(self.TypeFormatList[2])
		# た形
		self.WordStyleList.append(self.TypeFormatList[3])
		# 意志形
		self.WordStyleList.append(self.TypeFormatList[4])
		# 命令形
		if '・' in self.TypeFormatList[5]:
			self.WordStyleList.append(self.TypeFormatList[5].split('・')[0])
			self.WordStyleList.append(self.TypeFormatList[5].split('・')[1])
		else:
			self.WordStyleList.append(self.TypeFormatList[5])
		# 假定形
		self.WordStyleList.append(self.TypeFormatList[6])
		# 可能态
		# 一段动词 去る再变化
		self.WordStyleList.append(self.TypeFormatList[7][:-1])
		# 被动态
		# 一段动词 去る再变化
		self.WordStyleList.append(self.TypeFormatList[8][:-1])
		# 未然形
		# 形容词 去い再变化
		self.WordStyleList.append(self.TypeFormatList[9][:-1])
		# 使役态
		# 一段动词 去る再变化
		self.WordStyleList.append(self.TypeFormatList[10][:-1])
		# 使役被动态
		# 一段动词 去る再变化
		self.WordStyleList.append(self.TypeFormatList[11][:-1])
		# 禁止形
		self.WordStyleList.append(self.TypeFormatList[12])
		# ず形
		self.WordStyleList.append(self.TypeFormatList[13])

class I_Word(Comm_Word):
	def __init__(self, Word):
		super(I_Word, self).__init__()
		self.TypeNameList = ITypeNameList
		self.Word = Word
		self.Len = len(Word)
		self.WordStyleChangeLen = 1

	def SetTypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)
		# 连体形
		self.TypeFormatList.append(self.Word)
		# 副词化
		self.TypeFormatList.append(self.Word[:-1] + "く")
		# て形
		self.TypeFormatList.append(self.Word[:-1] + "くて")
		# た形
		self.TypeFormatList.append(self.Word[:-1] + "かった")
		# 未然形
		self.TypeFormatList.append(self.Word[:-1] + "くない")
		# 假定形
		self.TypeFormatList.append(self.Word[:-1] + "ければ")
		# です
		self.TypeFormatList.append(self.Word + "です")
		# 从句
		self.TypeFormatList.append(self.Word)

	def SetWordStyleList(self):
		self.WordStyleList.append(self.Word[:-1])

class Na_Word(Comm_Word):
	def __init__(self, Word):
		super(Na_Word, self).__init__()
		self.TypeNameList = NaTypeNameList
		self.Word = Word
		self.Len = len(Word)
		self.WordStyleChangeLen = 0

	def SetTypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)
		# 连体形
		self.TypeFormatList.append(self.Word + "な")
		# 副词化
		self.TypeFormatList.append(self.Word + "に")
		# て形
		self.TypeFormatList.append(self.Word + "で")
		# た形
		self.TypeFormatList.append(self.Word + "だった")
		# 未然形1
		self.TypeFormatList.append(self.Word + "ではない")
		# 未然形2
		self.TypeFormatList.append(self.Word + "じゃない")
		# 假定形
		self.TypeFormatList.append(self.Word + "であれば")
		# です
		self.TypeFormatList.append(self.Word + "です")
		# 从句
		self.TypeFormatList.append(self.Word + "な")

	def SetWordStyleList(self):
		# 原形
		self.WordStyleList.append(self.Word)

class N_Word(Comm_Word):
	def __init__(self, Word):
		super(N_Word, self).__init__()
		self.TypeNameList = NTypeNameList
		self.Word = Word
		self.Len = len(Word)
		self.WordStyleChangeLen = 0

	def SetTypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)
		# 连体形
		self.TypeFormatList.append(self.Word + "の")
		# て形
		self.TypeFormatList.append(self.Word + "で")
		# た形
		self.TypeFormatList.append(self.Word + "だった")
		# 未然形1
		self.TypeFormatList.append(self.Word + "ではない")
		# 未然形2
		self.TypeFormatList.append(self.Word + "じゃない")
		# 假定形
		self.TypeFormatList.append(self.Word + "であれば")
		# です
		self.TypeFormatList.append(self.Word + "です")
		# 从句
		self.TypeFormatList.append(self.Word + "な")

	def SetWordStyleList(self):
		# 原形
		self.WordStyleList.append(self.Word)

class A_Word(Comm_Word):
	def __init__(self, Word):
		super(A_Word, self).__init__()
		self.TypeNameList = ATypeNameList
		self.Word = Word
		self.Len = len(Word)
		self.WordStyleChangeLen = 0

	def SetTypeFormatList(self):
		# 原形
		self.TypeFormatList.append(self.Word)

	def SetWordStyleList(self):
		# 原形
		self.WordStyleList.append(self.Word)

class Japanese():
	def __init__(self):
		pass

	# 单词格式化
	# [引っ掛ける]ひっかける（他）：把……
	# ひっかける -> ひ か
	def WordFormat_init(self, Word, Hiragana):
		tmp = Word
		# 引っ掛ける -> (.)っ(.)ける
		id = 0
		while 1:
			result = re.sub(re.compile('(.*)([' + Pseudonym + ']*)([^' + Pseudonym + '\(\.\)])'), r'\1(.)', tmp)
			if result == tmp:
				break
			else:
				id += 1
				tmp=result

		# ひっかける -> ひ か
		if 1 == id:
			result = re.sub(re.compile(result), r'\1', Hiragana)
		elif 2 == id:
			result = re.sub(re.compile(result), r'\1 \2', Hiragana)
		elif 3 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3', Hiragana)
		elif 4 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3 \4', Hiragana)
		elif 5 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3 \4 \5', Hiragana)
		elif 6 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3 \4 \5 \6', Hiragana)
		elif 7 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3 \4 \5 \6 \7', Hiragana)
		elif 8 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3 \4 \5 \6 \7 \8', Hiragana)
		elif 9 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3 \4 \5 \6 \7 \8 \9', Hiragana)
		elif 10 == id:
			result = re.sub(re.compile(result), r'\1 \2 \3 \4 \5 \6 \7 \8 \9 \10', Hiragana)
		return result

	# [引っ掛ける]ひ か （他）：把…… -> [^引っ掛ける]:`引っ掛ける`:[引]^(ひ)っ[掛]^(か)ける（他）：把……
	def WordFormat(self, data):
		# 引っ掛ける
		Word = data.split(']')[0][1:]
		# ひっかける
		Hiragana = data.split(']')[1].strip()
		for flag in ['：','（']:
			if flag in Hiragana:
				Hiragana = Hiragana.split(flag)[0]

		# [すっかり]すっかり（0）：彻底得->[^すっかり]:`すっかり`:すっかり（0）：彻底得
		if Word == Hiragana:
			step1 = re.sub(r'\[([^\n]*)\]([^（：\n]*)', r'[^\1]:`\1`:\1', data)
			result = step1
			return result

		# [引っ掛ける]ひっかける（他）：把…… -> [引っ掛ける]ひ か（他）：把……
		if ' ' not in Hiragana:
			result = self.WordFormat_init(Word, Hiragana)
			data = data.replace(Hiragana, result)

		# ひ か
		# [^引っ掛ける]:`引っ掛ける`:[引っ掛ける]（他）：把……
		step1 = re.sub(r'\[([^\n]*)\]([^（：\n]*)', r'\2\n[^\1]:`\1`:[\1]', data)

		# ひ か
		# [^引っ掛ける]:`引っ掛ける`:[引っ掛ける]^()（他）：把……
		step2 = re.sub(r'\[([^\^]+)\]', r'[\1]^()', step1)

		# ひ か
		# [^引っ掛ける]:`引っ掛ける`:[引]^()[っ]^()[掛]^()[け]^()[る]^()（他）：把……
		tmp = step2
		while 1:
			step3 = re.sub(r'\[([^\^\(]+)([^\^\(]+)\]', r'[\1]^()[\2]', tmp)
			if step3 == tmp:
				break
			else:
				tmp=step3

		# ひ か
		# [^引っ掛ける]:`引っ掛ける`:[引]^()っ[掛]^()ける（他）：把……
		step4 = re.sub(re.compile('\[([' + Pseudonym + ']+)\]\^\(\)'), r'\1', step3)

		# [^引っ掛ける]:`引っ掛ける`:[引]^(ひ)っ[掛]^(か)ける（他）：把……
		tmp = step4
		while 1:
			step5 = re.sub(re.compile('([' + Pseudonym + ']+)[　 \n]+(.*)\(\)'), r'\n\2(\1)', tmp)
			if step5 == tmp:
				break
			else:
				tmp=step5
		result = step5[1:]
		#print(data)
		#print("1↓")
		#print(step1)
		#print("2↓")
		#print(step2)
		#print("3↓")
		#print(step3)
		#print("4↓")
		#print(step4)
		#print("5↓")
		#print(step5)
		#print("-------------------------------------")
		return result

	# 创建Word类
	def CreateWordClass(self, Word):
		ComWord = None
		if "い" == Word[-1]:
			#"イ形"
			ComWord = I_Word(Word)
		elif Word[-1] in "うくすつぬふむるぐずづぶぷ":
			ComWord = V_Word(Word)
		else:
			ComWord = N_Word(Word)
			#ComWord = Na_Word(Word)
			#ComWord = A_Word(Word)
		return ComWord

	def GetTypeName(self, Word):
		ComWord = self.CreateWordClass(Word)
		return ComWord.GetTypeNameList()

	def ChangeType(self, TypeNameList, Word):
		ComWord = self.CreateWordClass(Word)
		ComWord.SetTypeFormatList()
		return ComWord.GetTypeFormatList()

	# 句子注音
	def AnnotateSentence(self, data):
		KeyWords = re.sub(re.compile('([ 　、。?「」……:a-zA-Z々' + Pseudonym + ']+)'), r'|', data).strip('|')
		if 0 == len(KeyWords):
			return data

		cmd = "grep '\[\^' " + TanngoFile + " | awk -F'[:：（`＝]' '{print $3}' | grep -E \"" + KeyWords + "\" | sed 's/[々" + Pseudonym + KeyWords.strip('|') + "]/ /g' | sort | uniq | xargs | sed 's/ /|/g'"
		#print(cmd)
		ExpectWords = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()[0].decode().rstrip()
		cmd = "grep -n '\[\^' " + TanngoFile + " | awk -F'[:：（`＝]' '{print length($4)\",[\"$1\"],\"$4\",\"$6}' | grep -E \"" + KeyWords + "\" | sort"
		if len(ExpectWords) > 0:
			cmd = cmd + " | grep -vE \"" + ExpectWords + "\""
		print(cmd)
		results = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()

		annotate_list = []
		id = len(results)
		while id > 0:
			id -= 1
			line = results[id]
			print("    "+line.decode().rstrip().replace(',',":"))
			tmp_dict={}
			row = line.decode().rstrip().split(',')
			ComWord = self.CreateWordClass(row[2])
			ComWord.SetWordStyleList()
			change_len = ComWord.GetWordStyleChangeLen()
			if change_len > 0:
				tmp_dict['pattern'] = row[2][:-change_len]
				tmp_dict['annotate'] = row[3][:-change_len]
			else:
				tmp_dict['pattern'] = row[2]
				tmp_dict['annotate'] = row[3]
			tmp_dict['types'] = ComWord.GetWordStyleList()
			annotate_list.append(tmp_dict)

		tmp = data.replace(' ','').replace('　','')
		result = tmp
		for tmp_dict in annotate_list:
			#print(str(tmp_dict))
			for key in tmp_dict['types']:
				if key in tmp and "["+key+ "]" not in tmp:
					result = tmp.replace(tmp_dict['pattern'],tmp_dict['annotate'])
					tmp=result
					break
		#print(data)
		return result

class Markdown():
	def Example(self, data):
		step1 = re.sub(r'\[([^\]]*)\n\n([^\]]*)\]', r'<details>\n<summary>\1</summary>\n\n\2\n</details>\n', data)
		result = re.sub(r'\[([^\]]*)\n([^\]]*)\]', r'<details>\n<summary>\1</summary>\n\n\2\n</details>\n', step1)
		#print(data)
		#print("↓1")
		#print(step1)
		#print("↓2")
		#print(result)
		#print("-------------------------------------")
		return result

	def Annotate(self, data):
		tmp = data
		while 1:
			result = re.sub(r'(.*)\[([^\]]+)\]\^\(([^\)]]*)\)(.*)', r'\1<ruby>\2<rp>(</rp><rt>\3</rt><rp>)</rp></ruby>\4', data)
			if result == tmp:
				break
			else:
				tmp=result
		return result

def Usage():
	print('------------------------------------------------------------')
	print('Usage: python tool.py [mode]')
	print(' --help Show this help.')
	print(' [mode]:')
	print(' -fs [.md文件] : 句子格式化')
	print(' -fw [单词|.md文件] : 单词格式化')
	print(' -s [句子|.md文件] : 句子注音')
	print(' -c [单词,单词,单词] : 单词变形')
	print(' eg:')
	print(' python3 tool.py -fs tmp_fs.md')
	print(' python3 tool.py -fw [引っ掛ける]ひっかける（他）：把……')
	print(' python3 tool.py -fw tmp_fw.md')
	print(' python3 tool.py -s かぶきの切っ符を二枚もらったから、見に行きませんか。')
	print(' python3 tool.py -s tmp_s.md')
	print(' python3 tool.py -c 買う')
	print(' python3 tool.py -c 買う,飛んでくる,降りる,消す,休む,注ぐ,誤魔化す,受け取る,遊ぶ,了解する,増やす,注意する,直る,伝える,招く,来る,する')

__name__ = '__main__'
if __name__ == '__main__':
	argvs = sys.argv
	argc = len(argvs)
	if argc < 2:
		Usage()
		sys.exit(0)

	v=Japanese()
	mk=Markdown()
	mode = ""
	file = ""
	data = ""

	savefd = open(ResultFile, 'w', encoding='utf-8')
	# fd.write(self, str) 将str写入文件
	mode = argvs[1]
	if(os.path.exists(argvs[2])):
		file = argvs[2]
	else:
		data = argvs[2]

	if "-fs" == mode:
		if file:
			with open(argvs[2], 'r') as f:
				lines = f.read()
				#print(mk.Example(lines))
				savefd.write(mk.Example(lines) + '\n')

	elif "-fw" == mode:
		if file:
			with open(argvs[2], 'r') as f:
				lines = f.readlines()
				flag = 0
				for line in lines:
					line=line[:-1]
					savefd.write(v.WordFormat(line) + '\n')
		else:
			print(v.WordFormat(data))

	elif "-s" == mode:
		if file:
			with open(argvs[2], 'r') as f:
				lines = f.readlines()
				flag = 0
				for line in lines:
					line=line[:-1]
					if "</summary" in line:
						flag = 1
					elif "</details" in line:
						flag = 0
					elif 1 == flag and len(line) > 1:
						print("---------------------------------------------------------------------------------------------------------\n"+line)
						line = v.AnnotateSentence(line)
					savefd.write(line + '\n')
		if data:
			result = v.AnnotateSentence(data)
			savefd.write(result + '\n')

	elif "-c" == mode:
		if ',' in data:
			data_list = data.split(',')
			type = v.GetTypeName(data_list[0])
			savefd.write("|" + "|".join(type) + "|\n")
			savefd.write("|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n")
			for data in data_list:
				savefd.write("|" + "|".join(v.ChangeType(type, data)) + "|\n")
		else:
			type = v.GetTypeName(data)
			savefd.write("|" + "|".join(type) + "|\n")
			savefd.write("|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n")
			savefd.write("|" + "|".join(v.ChangeType(type, data)) + "|\n")




	#while len(argvs) > 1:
	#	myArgv = argvs.pop(1)	# 0th is this file's name
	#	if re.match('^\-\-help$', myArgv, re.IGNORECASE):
	#		Usage()
	#		sys.exit(0)
	#	elif re.match('^\-\-mode=(.+)$', myArgv, re.IGNORECASE):
	#		Param += myArgv + " "
	#		matchReg = re.match('^\-\-mode=(.+)$', myArgv, re.IGNORECASE)
	#		mode = matchReg.group(1)
	#	else:
	#		Usage()
	#		sys.exit('Invalid Parameter: ' + myArgv)
	if 0:
		print("AAAAAAAAAAAAAAAaa")
		print(mk.Annotate("引っ掛ける[引]^(ひ)っ[掛]^(か)ける：把……"))
		
		data="today is 01-11-2021."
		result1 = re.sub(r'(\d)-(\d)-(\d)', r'\3-\2-\1', data)
		result2 = re.sub(re.compile('(\d)-(\d)-(\d)'), '\3-\2-\1', data)
		print(data)
		print("↓")
		print(result1)
		print(result2)
		print("-------------------------------------")
	savefd.close()
