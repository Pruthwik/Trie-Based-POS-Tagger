"""Represent words in trie using training data with POS tags"""
from sys import argv
from re import search
import HeadNode

class Trie :

    def __init__(self, train_file, test_file, output_file) :
        try :
            self.train_file = train_file
            self.test_file = test_file
            self.output_file = output_file
            self.symbols = ['"', '.', ',', ':', ';', "'", '(', ')', '[', ']', '{', '}','|', '-', '_', '/', '\\']
            self.class_mapping = {'NN':0,'NST':1,'NNP':2,'PRP':3,'DEM':4,'VM':5,'VAUX':6,'JJ':7,'RB':8,\
'PSP':9,'RP':10,'CC':11,'WQ':12,'QF':13,'QC':14,'QO':15,'CL':16,'INTF':17,\
'INJ':18,'NEG':19,'UT':20,'SYM':21,'XC':22,'RDP':23,'ECH':24,'UNK':25}
        except IndexError :
            print("Insufficient Arguments : ")
            return

    def create_trie_using_train_and_predict_on_test(self) :
        """Read train file, create a trie, then predict POS on data in test file"""
        tot_words = 0
        head_prefix = HeadNode.HeadNode()
        head_suffix = HeadNode.HeadNode()
        with open(self.train_file, 'r', encoding = 'utf-8') as finp :
            words = finp.read().split()
            tot_words = len(words)
        for word in words :
            pos_tag = word[word.find('_') + 1 : ]
            word = word[ : word.find('_')]
            head_prefix.add_word(word.strip(), pos_tag)
            head_suffix.add_word(word[::-1], pos_tag)
            
        tflp = open(self.test_file, 'r', encoding='utf-8')
        oflp = open(self.output_file, 'a', encoding='utf-8')
        for line in tflp.readlines() :
            words_test = line.split()
            line_write = ''
            for word_test in words_test :
                pos_tag_write = ''
                flag = 0
                skip_index = 1
                prob_prefix = [0 for i in range(len(self.class_mapping))]
                prob_suffix = [0 for i in range(len(self.class_mapping))]
                prob_prefix = head_prefix.find_prob(word_test, prob_prefix, flag, skip_index)
                flag = 1
                skip_index = 1
                prob_suffix = head_suffix.find_prob(word_test[::-1], prob_suffix, flag, skip_index)
                prob_total = [prob_prefix[i] + prob_suffix[i] for i in range(len(self.class_mapping))]
                if max(prob_total) > 0 :
                    max_index = prob_total.index(max(prob_total))
                    for key, value in self.class_mapping.items():
                        if value == max_index :
                            pos_tag_write = key
                else :
                    if re.search('(\d+)(\.)?(\d+)?', word_test) is not None:
                        pos_tag_write = 'QF'
                    elif word_test in self.symbols :
                        pos_tag_write = 'SYM'
                    else :
                        pos_tag_write = 'UNK'
                line_write += word_test + '_' + pos_tag_write + ' '
            oflp.write(line_write.strip(' ') + '\n')
            line_write = ''


def main():
    """Pass arguments and call functions here."""    
    train_file = argv[1]
    test_file = argv[2]
    output_file = argv[3]
    trie = Trie(train_file, test_file, output_file)
    trie.create_trie_using_train_and_predict_on_test()


if __name__ == '__main__' :
    main()
