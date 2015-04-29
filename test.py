__author__ = 'ecowan'

import unittest
from spell_check import SpellCheck
from parser import Parser
from metrics import LocalMetrics, GlobalMetrics


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser("data/ch1.txt")

    def testTextString(self):
        self.assertIsNotNone(self.parser.text_string)

    def testLineSplit(self):
        self.assertEqual(self.parser.lines[0], 'Progris riport 1 marten 3.')


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

    def testResultDict(self):
        lexical_scores = self.local_metrics.lexical_score("Hello notaword", 1)
        self.assertEqual({'line_number': 1,
                          'line_score': 0.5,
                          'line_text': 'Hello notaword'}, lexical_scores)


class GlobalMetricsTest(unittest.TestCase):

    def setUp(self):
        #self.text = Parser("ch1.txt").lines
        self.text = "This is notaword also\nAnother lnie with invalid words".split("\n")
        self.global_metrics = GlobalMetrics()

    def testLexicalDiversity(self):
        diversity = self.global_metrics.lexical_diversity(["Hello this word once", "hello this word word twice"])
        self.assertEqual(None, diversity)

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