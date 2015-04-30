__author__ = 'ecowan'

import re


class Parser:

    def __init__(self, file_name):
        self.text_string = open(file_name, 'r').read()
        self.lines = [x for x in self.text_string.split('\n') if len(x) > 0]
        self.chapters = self.get_chapters()

    def get_chapters(self):
        return [x for x in re.compile('^Progris|^PROGRESS', re.MULTILINE).split(self.text_string) if len(x) > 0]
