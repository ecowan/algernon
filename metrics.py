__author__ = 'ecowan'

import re
from nltk import word_tokenize
from spell_check import SpellCheck


def average(input_list):
    return float(sum(input_list))/len(input_list) if len(input_list) > 0 else float('nan')

class LocalMetrics:
    '''
    Properties of the text on a line by line level
    '''

    def __init__(self):
        self.spell_check = SpellCheck()

    @staticmethod
    def fraction_punctuation(input_string):
        if len(input_string) > 0:
            return len(re.compile('\W+').findall(input_string))/float(len(input_string))
        else:
            return None

    @staticmethod
    def fraction_quotes(input_string):
        if len(input_string) > 0:
            quotes = len([x for x in input_string if x=='"'])
            return quotes/float(len(input_string))
        else:
            return None

    @staticmethod
    def quotes_length(input_string):
        quotes = [a for i,a in enumerate(input_string.split('"')) if i>0 and i%3 == 0 or i==1]
        if len(quotes) == 0:
            return 0
        else:
            return sum([len(x) for x in quotes])/float(len(quotes))

    def lexical_score(self, line, line_number):
        correct = self.spell_check.fraction_correct(line)
        return {'line_number': line_number,
                'line_text': line,
                'line_score': correct}


class Diversity:

    def __init__(self, input_string, bin_size):
        self.spell_check = SpellCheck()
        self.input_string = input_string
        self.words = word_tokenize(input_string)
        self.word_bins = self.split_into_bins(bin_size)

    def split_into_bins(self, bin_size):
        return [self.words[bin_size*i:bin_size*(i+1)] for i in range(0, len(self.words)/bin_size)]

    @staticmethod
    def _lexical_diversity(word_list):
        if len(word_list) > 0:
            # print set(word_list), word_list, {'fraction_unique_words': len(set(word_list))/float(len(word_list))}
            return {'fraction_unique_words': len(set(word_list))/float(len(word_list))}
        else:
            return {'fraction_unique_words': 0.0}

    def fraction_unique_words_per_bin(self):
        return [(i, self._lexical_diversity(w)) for (i,w) in enumerate(self.word_bins)]

    def fraction_unique_words(self, string_list):
        return [(i, self._lexical_diversity(w)) for (i,w) in enumerate(string_list)]

    def fraction_unique_valid_words(self, string_list):
        string_list = [self.spell_check.filter_invalid_words(x) for x in string_list]
        return self.fraction_unique_words(string_list)

class GlobalMetrics:
    '''
    Properties of the text on a chapter level
    '''
    def __init__(self):
        self.local_metrics = LocalMetrics()

    def unique_words(self, string_list):
        return

    def lexical_scores(self, lines):
        return [self.local_metrics.lexical_score(line, index) for (index, line) in enumerate(lines)]

    def split_into_bins(self, lexical_scores, bin_size):
        return [[x for x in lexical_scores[bin_size*i:bin_size*(i+1)]] for i in range(0, len(lexical_scores)/bin_size)]

    @staticmethod
    def bin_scores(bins):
        return [map(lambda x: x['line_score'], b) for b in bins]

    @staticmethod
    def bin_averages(bin_scores):
        return [average(x) for x in bin_scores]

    def metrics(self, lines, bin_size):
        lexical_scores = self.lexical_scores(lines)
        bins = self.split_into_bins(lexical_scores, bin_size)
        bin_scores = self.bin_scores(bins)
        bin_averages = self.bin_averages(bin_scores)
        return {'bin_averages': [(i,x) for (i,x) in enumerate(bin_averages)]}
