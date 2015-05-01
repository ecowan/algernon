__author__ = 'ecowan'

import unittest
from spell_check import SpellCheck
from parser import Parser
from metrics import LocalMetrics, Diversity, GlobalMetrics


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser("data/ch1.txt")

    def testTextString(self):
        self.assertIsNotNone(self.parser.text_string)

    def testLineSplit(self):
        self.assertEqual(self.parser.lines[0], 'Progris riport 1 marten 3.')

    def testChapterSplit(self):
        self.chapters = Parser("data/full_text.txt").chapters
        self.assertEqual(17, len(self.chapters))


class SpellCheckTest(unittest.TestCase):

    def setUp(self):
        self.spell_check = SpellCheck()

    def testResultIsDecimal(self):
        self.assertIsInstance(self.spell_check.fraction_correct("Hello there"), float)

    def testResultIsHalf(self):
        self.assertEqual(0.5, self.spell_check.fraction_correct("Hello thre"))


class LocalMetricsTest(unittest.TestCase):

    def setUp(self):
        self.local_metrics = LocalMetrics()

    def testPunctuationFraction(self):
        self.assertEqual(0.2, self.local_metrics.fraction_punctuation("test."))

    def testQuoteFraction(self):
        self.assertEqual(0.25, self.local_metrics.fraction_quotes('"Hi"'))

    def testQuoteLength(self):
        self.assertEqual(0.64, self.local_metrics.quotes_length('"I said something" I said'))

    def testResultDict(self):
        lexical_scores = self.local_metrics.lexical_score("Hello notaword", 1)
        self.assertEqual({'line_number': 1,
                          'line_score': 0.5,
                          'line_text': 'Hello notaword'}, lexical_scores)


class DiversityTest(unittest.TestCase):

    def setUp(self):
        self.chapters = Parser("data/full_text.txt").chapters
        self.input_string = "Hi this is a sentence. This is also a sentence"
        self.diversity = Diversity(self.input_string, 10)

    def testFraction(self):
        unique_fraction = self.diversity.fraction_unique_words([self.input_string])
        self.assertEqual([(0, {'fraction_unique_words': 0.30434782608695654})], unique_fraction)

    def testFractionUniqueValid(self):
        unique_fraction_valid = self.diversity.fraction_unique_valid_words(self.chapters)
        self.assertEqual((0, {'fraction_unique_words': 0.5028901734104047}), unique_fraction_valid[0])

class GlobalMetricsTest(unittest.TestCase):

    def setUp(self):
        #self.text = Parser("ch1.txt").lines
        self.text = "This is notaword also\nAnother lnie with invalid words".split("\n")
        self.global_metrics = GlobalMetrics()

    def testResultDict(self):
        lexical_scores = self.global_metrics.lexical_scores(self.text)
        self.assertEqual({'line_number': 0,
                          'line_score': 0.75,
                          'line_text': 'This is notaword also'}, lexical_scores[0])

    def testSplitIntoBins(self):
        lexical_scores = self.global_metrics.lexical_scores(self.text)
        bins = self.global_metrics.split_into_bins(lexical_scores, 2)
        self.assertEqual({'line_number': 0,
                          'line_score': 0.75,
                          'line_text': 'This is notaword also'}, bins[0][0])

    def testBinScores(self):
        lexical_scores = self.global_metrics.lexical_scores(self.text)
        bins = self.global_metrics.split_into_bins(lexical_scores, 2)
        bin_scores = self.global_metrics.bin_scores(bins)
        self.assertEqual([0.75, 0.8], bin_scores[0])

    def testBinAverages(self):
        lexical_scores = self.global_metrics.lexical_scores(self.text)
        bins = self.global_metrics.split_into_bins(lexical_scores, 2)
        bin_scores = self.global_metrics.bin_scores(bins)
        bin_averages = self.global_metrics.bin_averages(bin_scores)
        self.assertEqual(0.775, bin_averages[0])