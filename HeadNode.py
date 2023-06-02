"""HeadNode for POS tagging."""
import CharNode

class HeadNode :

	def __init__(self) :
		self.root_nodes = dict()

	def add_word(self, word, pos_tag) :
		word = word.strip()
		if len(word) == 0:
			return
		cnode = self.root_nodes.get(word[0])
		if cnode is None :
			cnode = CharNode.Char_Node()
			cnode.char = word[0]
			if word[0]:
				self.root_nodes[word[0]] = cnode
		cnode.add_word(word, pos_tag, 0)

	def view_node(self, level) :
		print('Head Nodes : ')
		for root in self.root_nodes :
			print('Head =', root)
			node = self.root_nodes.get(root)
			node.view_node(0)

	def find_prob(self, word, prob, flag, skip_index) :
		if len(word) > 0:
			node = self.root_nodes.get(word[0])
			if node is not None :
				prob = node.find_prob(word, 0, prob, flag, skip_index)
				return prob
			else:
				return prob
			

