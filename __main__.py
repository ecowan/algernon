__author__ = 'ecowan'

from parser import Parser
from metrics import LocalMetrics, GlobalMetrics, Diversity
import matplotlib.pyplot as plt


class Plot:

    def __init__(self):
        self.parser = Parser("data/full_text.txt")
        self.local_metrics = LocalMetrics()
        self.global_metrics = GlobalMetrics()
        self.diversity = Diversity(self.parser.text_string, 2000)
        self.lines = self.parser.lines
        self.chapters = self.parser.chapters
        self.chapter_bins = range(1, len(self.chapters)+1)

    def set_figure(self, index=None):
        if index:
            plt.figure(index)
        else:
            pass

    def plot_average_line_score(self, index=None):
        self.set_figure(index)
        averages = self.global_metrics.metrics(self.chapters, 1)['bin_averages']
        bins = [x[0] for x in averages]
        averages = [x[1] for x in averages]
        plt.plot(bins, averages, 'b-o')
        plt.title("Average number of correctly spelled words")
        plt.xlabel("Chapter")
        plt.ylabel("Average correct words")
        plt.savefig('average_line_score')

    def plot_diversity(self, index=None):
        self.set_figure(index)
        unique_valid_words = self.diversity.fraction_unique_valid_words(self.chapters)
        bins = [x[0]+1 for x in unique_valid_words]
        scores = [x[1]['fraction_unique_words'] for x in unique_valid_words]
        plt.plot(bins, scores, 'b-o')
        plt.title("Lexical Diversity")
        plt.xlabel("Chapter")
        plt.ylabel("Fraction of unique words")
        plt.savefig('lexical_diversity')

    def plot_quotes_per_chapter(self, index=None):
        self.set_figure(index)
        quotes_per_chapter = [self.local_metrics.fraction_quotes(x) for x in self.chapters]
        plt.plot(self.chapter_bins, quotes_per_chapter, 'b-o')
        plt.title("Fraction of quote characters")
        plt.xlabel("Chapter")
        plt.ylabel("Fraction of quote characters")
        plt.savefig('quotes_per_chapter')

    def plot_average_quote_length(self, index=None):
        self.set_figure(index)
        quote_length_per_chapter = [self.local_metrics.quotes_length(x) for x in self.chapters]
        plt.plot(self.chapter_bins, quote_length_per_chapter, 'b-o')
        plt.title("Average quote length")
        plt.xlabel("Chapter")
        plt.ylabel("Average quote length (characters)")
        plt.savefig('average_quote_length')

def main():

    plotter = Plot()
    plotter.plot_average_line_score(1)
    plotter.plot_diversity(2)
    plotter.plot_quotes_per_chapter(3)
    plotter.plot_average_quote_length(4)

    #    print "Unique valid words per chapter:\n", unique_valid_words
    #plot_diversity(unique_valid_words)
    #plt.plot(bins, avgs, 'r-')
    #plt.show()


if __name__ == "__main__":
    main()