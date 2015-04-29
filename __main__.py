__author__ = 'ecowan'

from parser import Parser
from metrics import GlobalMetrics, Diversity
import matplotlib.pyplot as plt


def plot_diversity(fraction_unique_words):
    bins = [x[0] for x in fraction_unique_words]
    scores = [x[1]['fraction_unique_words'] for x in fraction_unique_words]
    plt.plot(bins, scores, 'g-o')
    plt.show()

def main():
    parser = Parser("data/full_text.txt")
    lines = parser.lines
    global_metrics = GlobalMetrics()
    averages = global_metrics.metrics(lines, 10)['bin_averages']
    print averages
    bins = [x[0] for x in averages]
    avgs = [x[1] for x in averages]
    #print bins

    diversity = Diversity(parser.text_string, 5000)
    print diversity.fraction_unique_words()
    plot_diversity(diversity.fraction_unique_words())

    #plt.plot(bins, avgs, 'r-')
    #plt.show()


if __name__ == "__main__":
    main()