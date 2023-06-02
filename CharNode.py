"""Char Node for representing words for POS Tagging."""
class Char_Node :
	
	def __init__(self) :
		self.class_map = {'NN':0,'NST':1,'NNP':2,'PRP':3,'DEM':4,'VM':5,'VAUX':6,'JJ':7,'RB':8,\
'PSP':9,'RP':10,'CC':11,'WQ':12,'QF':13,'QC':14,'QO':15,'CL':16,'INTF':17,\
'INJ':18,'NEG':19,'UT':20,'SYM':21,'XC':22,'RDP':23,'ECH':24,'UNK':25}
		self.POS = dict()
		self.prefix = dict()
		self.suffix = dict()
		self.next_node = dict()
		self.char = ''
		
	def add_word(self, word, pos_tag, curr_ind) :
		
		pos_tag_index = self.class_map.get(pos_tag)
		if pos_tag_index not in self.POS :
			self.POS[pos_tag_index] = 1
		else :
			self.POS[pos_tag_index] = self.POS.get(pos_tag_index) + 1
		prefix = word[: curr_ind + 1]
		suffix = word[len(word) - 1 - curr_ind : ]
		if prefix not in self.prefix :
			self.prefix[prefix] = 1
		else:
			self.prefix[prefix] = self.prefix.get(prefix) + 1

		if suffix not in self.suffix :
			self.suffix[suffix] = 1
		else:
			self.suffix[suffix] = self.suffix.get(suffix) + 1
		curr_ind += 1
		if curr_ind < len(word) :
			node = self.next_node.get(word[curr_ind])
			if node is None :
				node = Char_Node()
				node.char = word[curr_ind]
				self.next_node[word[curr_ind]] = node
			node.add_word(word, pos_tag, curr_ind)
		
	def view_node(self, level) :
		print("Level",level,"entries",self.char, self.POS, self.prefix, self.suffix)
		for node in self.next_node.values() :
			node.view_node(level + 1)

	def find_prob(self, word, curr_ind, prob, flag, skip_index) :
		if flag == 0 :
			#print('Prefix Trie :')
			if self.char != '':
				if self.POS is not None :
					class_indices = list(self.POS.keys())
					values = list(self.POS.values())
					tot = sum(values)
					if tot > 0 :
						for i in class_indices :
							if self.POS.get(i) is not None and (len(word) <= skip_index + 1 or \
(curr_ind >= skip_index and curr_ind <= skip_index + 2)):
								if prob[i] != 0 :
									prob[i] = prob[i] + prob[i] * (self.POS.get(i) / tot)
								else :
									prob[i] = self.POS.get(i) / tot
							else :
								break

					curr_ind += 1
					print(curr_ind)
					print(word)
					print(prob)
					if curr_ind < len(word) :
						node = self.next_node.get(word[curr_ind])
						if node is not None :
							node.find_prob(word, curr_ind, prob, flag, skip_index)
		else :
			if self.char != '':
				if self.POS is not None :
					class_indices = list(self.POS.keys())
					values = list(self.POS.values())
					tot = sum(values)
					if tot > 0 :
						for i in class_indices :
							if self.POS.get(i) is not None and curr_ind <= skip_index + 2:
								if prob[i] != 0 :
									prob[i] = prob[i] + prob[i] * (self.POS.get(i) / tot)
								else :
									prob[i] = self.POS.get(i) / tot
						curr_ind += 1
					if curr_ind < len(word) :
						node = self.next_node.get(word[curr_ind])
						if node is not None :
							node.find_prob(word, curr_ind, prob, flag, skip_index)
		#print(prob.index(max(prob)))
		#print(prob)
		return prob
				


				

		

