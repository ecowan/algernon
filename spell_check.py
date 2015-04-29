__author__ = 'ecowan'

import enchant
from nltk import word_tokenize


class SpellCheck:

    def __init__(self):
        self.d = enchant.Dict("en_US")

    def fraction_correct(self, input_string):
        '''
        Fraction of words in text that are valid English
        :return:
        '''
        words = word_tokenize(input_string)
        correct = [x for x in words if self.d.check(x)]
        return len(correct)/float(len(words))
