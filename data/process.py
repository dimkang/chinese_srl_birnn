import json
import collections

max_dis = -1
min_dis = 1000

def splitFile(filename):
	f = open(filename)
	lines = f.readlines()
	retLines = []
	for line in lines:
		tokens = line.split(' ')
		words = []
		poss = []
		srs = []
		for wps in tokens:
			if wps == '\n' or wps == '':
				continue
			tokens = wps.split('/')
			word = tokens[0]
			pos = tokens[1]
			if len(tokens) == 3:
				sr = tokens[2]
			else:
				sr = 'O'
			words.append(word)
			poss.append(pos)
			srs.append(sr)
		retLines.append({'words': words, 'poss': poss, 'srs': srs})
	return retLines

def makeDict(data, key, saveFile):
	tokens = []
	for line in data:
		tokens.extend(line[key])
	counter = collections.Counter(tokens)
	count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
	count_pairs.insert(0, ('<PAD>', 0))
	f = open(saveFile, 'w')
	for i in range(len(count_pairs)):
		f.write(str(count_pairs[i][0]) + '\t' + str(i) + '\n')
	f.close()

def generateInput(data, saveFile):
	global max_dis
	global min_dis
	f = open(saveFile, 'w')
	for line in data:
		words = line['words']
		poss = line['poss']
		srs = line['srs']
		for i in range(len(words)):
			if srs[i] == 'rel':
				rel_index = i
				rel = words[i]
		for i in range(len(words)):
			word = words[i]
			left_word = '<PAD>'
			if i > 0:
				left_word = words[i-1]
			right_word = '<PAD>'
			if i < len(words) - 1:
				right_word = words[i+1]
			pos = poss[i]
			left_pos = '<PAD>'
			if i > 0:
				left_pos = poss[i-1]
			right_pos = '<PAD>'
			if i < len(poss) - 1:
				right_pos = poss[i+1]
			rel_distance = abs(rel_index - i)
			if max_dis < rel_distance:
				max_dis = rel_distance
			if min_dis > rel_distance:
				min_dis = rel_distance
			sr = srs[i]
			f.write(word + '\t' + left_word + '\t' + right_word + '\t' + 
				pos + '\t' + left_pos + '\t' + right_pos + '\t' + 
				rel + '\t' + str(rel_distance) + '\t' + sr + '\n')
		f.write('\n')
	f.close()

data = splitFile('cpbtrain.txt')
#makeDict(data, 'words', 'word2id')
#makeDict(data, 'srs', 'label2id')
generateInput(data, 'train.in')
data = splitFile('cpbdev.txt')
generateInput(data, 'validation.in')
data = splitFile('cpbtest.txt')
generateInput(data, 'test.in')
print(max_dis)
print(min_dis)