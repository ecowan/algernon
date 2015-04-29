__author__ = 'ecowan'

from spell_check import SpellCheck


def average(input_list):
    return float(sum(input_list))/len(input_list) if len(input_list) > 0 else float('nan')

class LocalMetrics:

    def __init__(self):
        self.spell_check = SpellCheck()

    def lexical_score(self, line, line_number):
        return {'line_number': line_number,
                'line_text': line,
                'line_score': self.spell_check.fraction_correct(line)}


class GlobalMetrics:

    def __init__(self):
        self.local_metrics = LocalMetrics()

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


'''
    def split_into_bins(self, lexical_scores, bin_size):
        result = []
        for i,x in enumerate(lexical_scores):
            if i % bin_size == 0:
                result.append([])
                result[-1].append(x)
            else:
                result[-1].append(x)
'''