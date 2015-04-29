__author__ = 'ecowan'


class Parser:

    def __init__(self, file_name):
        self.text_string = open(file_name, 'r').read()
        self.lines = [x for x in self.text_string.split('\n') if len(x) > 0]

    def get_chapters(self):
        '''
        Split on month names probably, from June to November
        :return:
        '''
        pass