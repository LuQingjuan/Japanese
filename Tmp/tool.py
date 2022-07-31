import re
import os
import sys
import subprocess

TanngoFile = "Tanngo.md"
ResultFile = "Result.md"

class VChange():
	def __init__(self):
		self.Allflag="あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっ"
		#            アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッーィェ

		self.Sort={"う":0, "く":1, "す":2, "つ":3, "ぬ":4, "ふ":5, "む":6, "る":7, "ぐ":8, "ず":9, "づ":10, "ぶ":11, "ぷ":12}
		self.Table=[["あ","い","う","え","お"],
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

		self.VType=["原形", "假定形", "ます形", "て形", "た形", "意志形", "命令形","可能态","被动态", "未然形", '使役态',"使役被动态"]
		self.VWordType=["五段","一段","カ变","サ变","イ形","ナ形","Ｎ词",""]
		self.VFlag=["う","く","す","つ","ぬ","ふ","む","る","ぐ","ず","づ","ぶ","ぷ"]
		self.VSpecialFlag="いえきけしせちてにねひへみめりれぎげじぜぢでびべぴぺ"

	def GetWordType(self, Word):
		if "い" == Word[-1]:
			#"イ形"
			return self.VWordType[4]
		elif Word[-1] in self.VFlag:
			if "する" == Word[-2:]:
				#"サ变"
				return self.VWordType[3]
			elif "くる" == Word[-2:] or "来る" == Word[-2:]:
				#"カ变"
				return self.VWordType[2]
			elif "る" == Word[-1] and Word[-2] in self.VSpecialFlag:
				#"一段"
				return self.VWordType[1]
			else:
				#"知る","要る","入る","煎る","炒る","蹴る","減る","散る","練る","照る","切る","混じる","区切る","千切る","裏切る"]
				#"五段"
				return self.VWordType[0]
		else:
			return self.VWordType[7]

	def ChangeIType(self, Word):
		type = self.GetWordType(Word)
		Words=[]
		#"原形"
		Words.append(Word)
		Words.append(Word[:-1] + "く")
		Words.append(Word[:-1] + "か" + "った")
		return Words

	def ChangeITypeNoFlag(self, Word):
		Words=self.ChangeIType(Word)
		return Words

	def ChangeVType(self, Word):
		type = self.GetWordType(Word)
		Words=[]
		#"原形"
		Words.append(Word)
		#"假定形"
		Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][3] + "ば")
		if "五段" == type:
			#"ます形"
			Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][1] + "ます")
			#"て形"
			if   "う" == Word[-1] or "つ" == Word[-1] or "る" == Word[-1]:
				Words.append(Word[:-1] + "って")
			elif "む" == Word[-1] or "ぶ" == Word[-1] or "ぬ" == Word[-1]:
				Words.append(Word[:-1] + "んで")
			elif "く" == Word[-1]:
				if "行く" == Word:
					Words.append(Word[:-1] + "って")
				else:
					Words.append(Word[:-1] + "いて")
			elif "ぐ" == Word[-1]:
				Words.append(Word[:-1] + "いで")
			elif "す" == Word[-1]:
				Words.append(Word[:-1] + "して")
			#"た形"
			if   "う" == Word[-1] or "つ" == Word[-1] or "る" == Word[-1]:
				Words.append(Word[:-1] + "った")
			elif "む" == Word[-1] or "ぶ" == Word[-1] or "ぬ" == Word[-1]:
				Words.append(Word[:-1] + "んだ")
			elif "く" == Word[-1]:
				if "行く" == Word:
					Words.append(Word[:-1] + "った")
				else:
					Words.append(Word[:-1] + "いた")
			elif "ぐ" == Word[-1]:
				Words.append(Word[:-1] + "いだ")
			elif "す" == Word[-1]:
				Words.append(Word[:-1] + "した")
			#"意志形"
			Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][4] + "う")
			#"命令形"
			Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][3])
			#"可能态"
			Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][3] + "る")
			#"被动态"
			if "う" == Word[-1]:
				Words.append(Word[:-1] + "わ" + "れる")
			else:
				Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][0] + "れる")
			#"未然形"
			if "ある" == Word:
				Words.append("ない")
			elif "う" == Word[-1]:
				Words.append(Word[:-1] + "わ" + "ない")
			else:
				Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][0] + "ない")
			#'使役态'
			if "う" == Word[-1]:
				Words.append(Word[:-1] + "わ" + "せる")
			else:
				Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][0] + "せる")
			#"使役被动态"
			if "す" == Word[-1]:
				Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][0] + "せられる")
			elif "う" == Word[-1]:
				Words.append(Word[:-1] + "わ" + "される")
			else:
				Words.append(Word[:-1] + self.Table[self.Sort[Word[-1]]][0] + "される")
		elif "一段" == type:
			#"ます形"
			Words.append(Word[:-1] + "ます")
			#"て形"
			Words.append(Word[:-1] + "て")
			#"た形"
			Words.append(Word[:-1] + "た")
			#"意志形"
			Words.append(Word[:-1] + "よう")
			#"命令形"
			Words.append(Word[:-1] + "ろ")
			#"可能态"
			Words.append(Word[:-1] + "られる")
			#"被动态"
			Words.append(Word[:-1] + "られる")
			#"未然形"
			Words.append(Word[:-1] + "ない")
			#'使役态'
			Words.append(Word[:-1] + "させる")
			#"使役被动态"
			Words.append(Word[:-1]  + "させられる")
		elif "カ变" == type:
			#"ます形"
			Words.append(Word[:-2] + "きます")
			#"て形"
			Words.append(Word[:-2] + "きて")
			#"た形"
			Words.append(Word[:-2] + "きた")
			#"意志形"
			Words.append(Word[:-2] + "こよう")
			#"命令形"
			Words.append(Word[:-2] + "こい")
			#"可能态"
			Words.append(Word[:-2] + "こられる")
			#"被动态"
			Words.append(Word[:-2] + "こられる")
			#"未然形"
			Words.append(Word[:-2] +"こない")
			#'使役态'
			Words.append(Word[:-2] +"こさせる")
			#"使役被动态"
			Words.append(Word[:-2] +"こさせられる")
		elif "サ变" == type:
			#"ます形"
			Words.append(Word[:-2] +"します")
			#"て形"
			Words.append(Word[:-2] +"して")
			#"た形"
			Words.append(Word[:-2] +"した")
			#"意志形"
			Words.append(Word[:-2] +"しよう")
			#"命令形"
			Words.append(Word[:-2] +"しろ")
			#"可能态"
			Words.append(Word[:-2] +"できる")
			#"被动态"
			Words.append(Word[:-2] +"される")
			#"未然形"
			Words.append(Word[:-2] +"しない")
			#'使役态'
			Words.append(Word[:-2] +"させる")
			#"使役被动态"
			Words.append(Word[:-2] +"させられる")
		print(type)
		return Words

	def ChangeVTypeNoFlag(self, Word):
		Words=self.ChangeVType(Word)
		type = self.GetWordType(Word)
		if "サ变" == type:
			#"原形"
			Words[0] = Words[0][:-2]
		#"原形"
		#Words[0] = Words[0]
		#"假定形"
		#Words[1] = Words[1][:-1]
		#"ます形"
		Words[2] = Words[2][:-1]
		#"て形"
		#Words[3] = Words[3]
		#"た形"
		#Words[4] = Words[4]
		#"意志形"
		#Words[5] = Words[5]
		#"命令形"
		#Words[6] = Words[6]
		#"可能态"
		Words[7] = Words[7][:-1]
		#"被动态"
		Words[8] = Words[8][:-1]
		#"未然形"
		Words[9] = Words[9][:-1]
		#'使役态'
		Words[10] = Words[10][:-1]
		#Words.append(Word[:-2] +"させる")
		#"使役被动态"
		Words[11] = Words[11][:-1]
		#print(str(Words))
		return Words

	# 单词格式化
	# [引っ掛ける]ひっかける（他）：把……
	# ひっかける -> ひ か
	def WordFormat_init(self, Word, Hiragana):

		tmp = Word
		# 引っ掛ける -> (.)っ(.)ける
		id = 0
		while 1:
			result = re.sub(r'(.*)([あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッーィェ]*)([^あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッーィェ\(\.\)])', r'\1(.)', tmp)
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
			step1 = re.sub(r'\[([^\n]*)\]([^（：\n]*)', r'[^\1]:`\1`:', data)
			result = step1
			return result

		# [引っ掛ける]ひっかける（他）：把…… -> [引っ掛ける]ひ か（他）：把……
		if ' ' not in Hiragana:
			result = self.WordFormat_init(Word, Hiragana)
			data =  data.replace(Hiragana, result)

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
		step4 = re.sub(r'\[([アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユェヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポィェャュョッーあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっ]+)\]\^\(\)', r'\1', step3)

		# [^引っ掛ける]:`引っ掛ける`:[引]^(ひ)っ[掛]^(か)ける（他）：把……
		tmp = step4
		while 1:
			step5 = re.sub(r'([アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユェヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポィェャュョッーあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっ]+)[　 \n]+(.*)\(\)', r'\n\2(\1)', tmp)
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

	# 句子注音
	def AnnotateSentence(self, data):
		KeyWords = re.sub(r'([ 　、。?「」……:々あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッーィェ]+)', r'|', data).strip('|')
		if 0 == len(KeyWords):
			return data

		cmd = "grep '\[\^' " + TanngoFile + " | awk -F'[:：（`＝]' '{print $3}' | grep -E \"" + KeyWords + "\" | sed 's/[々あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッーィェ" + KeyWords.strip('|') + "]/ /g' | sort | uniq | xargs | sed 's/ /|/g'"
		#print(cmd)
		ExpectWords = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()[0].decode().rstrip()
		cmd = "grep -n '\[\^' " + TanngoFile + " | awk -F'[:：（`＝]' '{print $1\",\"$4\",\"$6}' | grep -E \"" + KeyWords + "\""
		if len(ExpectWords) > 0:
			cmd = cmd + " | grep -vE \"" + ExpectWords + "\""
		print(cmd)
		results = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()

		annotate_list=[]
		for line in results:
			print("    "+line.decode().rstrip().replace(',',":"))
			tmp_dict={}
			row = line.decode().rstrip().split(',')
			word = row[1]
			type = self.GetWordType(word)
			if "イ形" == type:
				tmp_dict['pattern'] = row[1][:-1]
				tmp_dict['annotate'] = row[2][:-1]
				tmp_dict['types'] = self.ChangeIType(word)
			elif "五段" == type or "一段" == type:
				tmp_dict['pattern'] = row[1][:-1]
				tmp_dict['annotate'] = row[2][:-1]
				tmp_dict['types'] = self.ChangeVTypeNoFlag(word)
			elif "カ变" == type or "サ变" == type:
				tmp_dict['pattern'] = row[1][:-2]
				tmp_dict['annotate'] = row[2][:-2]
				tmp_dict['types'] = self.ChangeVTypeNoFlag(word)
			else:
				tmp_dict['pattern'] = row[1]
				tmp_dict['annotate'] = row[2]
				tmp_dict['types'] = [row[1]]
			annotate_list.append(tmp_dict)

		tmp = data
		result = data
		for tmp_dict in annotate_list:
			#print(str(tmp_dict))
			for key in tmp_dict['types']:
				if key in tmp and "["+key[:-1]+"]" not in tmp:
					result = tmp.replace(tmp_dict['pattern'],tmp_dict['annotate'])
					tmp=result
					break
		#print(data)
		return result

class Markdown():
	def Example(self, data):
		result = re.sub(r'\[([^\]]*)\n([^\]]*)\]', r'<details>\n<summary>\1</summary>\n\n\2\n</details>\n', data)
		#print(data)
		#print("↓")
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
	print('  --help  Show this help.')
	print('  [mode]:')
	print('    -fs [.md文件]                      : 句子格式化')
	print('    -fw [单词|.md文件]                 : 单词格式化')
	print('    -s [句子|.md文件]                 : 句子注音')
	print('    -c [单词,单词,单词]                : 单词变形')
	print('       eg:')
	print('           python3 tool.py -fs tmp_fs.md')
	print('           python3 tool.py -fw [引っ掛ける]ひっかける（他）：把……')
	print('           python3 tool.py -fw tmp_fw.md')
	print('           python3 tool.py -s かぶきの切っ符を二枚もらったから、見に行きませんか。')
	print('           python3 tool.py -s tmp_s.md')
	print('           python3 tool.py -c 買う')
	print('           python3 tool.py -c 買う,飛んでくる,降りる,消す,休む,注ぐ,誤魔化す,受け取る,遊ぶ,了解する,増やす,注意する,直る,伝える,招く,来る,する')

__name__ = '__main__'
if __name__ == '__main__':
	argvs = sys.argv
	argc = len(argvs)
	if argc < 2:
		Usage()
		sys.exit(0)

	v=VChange()
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
						print("--------------------------------------------------------\n"+line)
						line = v.AnnotateSentence(line)
					savefd.write(line + '\n')
		if data:
			result = v.AnnotateSentence(data)
			savefd.write(result + '\n')

	elif "-c" == mode:
		savefd.write("|" + "|".join(v.VType) + "|\n")
		savefd.write("|-|-|-|-|-|-|-|-|-|-|-|-|\n")
		if ',' in data:
			data_list = data.split(',')
			for data in data_list:
				savefd.write("|" + "|".join(v.ChangeVType(data)) + "|\n")
		else:
			savefd.write("|" + "|".join(v.ChangeVType(data)) + "|\n")



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
