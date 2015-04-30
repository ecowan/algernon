__author__ = 'ecowan'

import logging
import enchant
from nltk import word_tokenize

def logger():
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('debug.log')
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


class SpellCheck:

    def __init__(self, logger=logger()):
        self.d = enchant.Dict("en_US")
        self.logger = logger

    def valid_word(self, word):
        return self.d.check(word)

    def count_valid_words(self, input_string):
        return len([x for x in word_tokenize(input_string) if self.valid_word(x)])

    def filter_invalid_words(self, input_string):
        if len(input_string) > 0:
            return [x for x in word_tokenize(input_string) if self.d.check(x)]
        else:
            return ''

    def fraction_correct(self, input_string):
        '''
        Fraction of words in text that are valid English
        :return:
        '''
        words = word_tokenize(input_string)
        correct = [x for x in words if self.d.check(x)]
        fraction = len(correct)/float(len(words))
        self.logger.debug("%s\t%s", input_string, str(fraction))
        #print input_string, fraction
        return fraction
