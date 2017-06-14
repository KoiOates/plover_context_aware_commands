#!/usr/bin/env python

import re
import os
import subprocess


## Begin abridged snippet of Suggestions dialogue code
class PreviousTranslations():
    WORDS_RX = re.compile(r'[-\'"\w]+|[^\w\s]')
    def __init__(self):
        self._words = u''
        self.last_individual_words = u''

    @staticmethod
    def tails(ls):
        ''' Return all tail combinations (a la Haskell)

            tails :: [x] -> [[x]]
            >>> tails('abcd')
            ['abcd', 'bcd', 'cd', d']

        '''

        for i in range(len(ls)):
            yield ls[i:]

    def on_translation(self, old, new):
        for action in old:
            remove = len(action.text)
            if remove > 0:
                self._words = self._words[:-remove]
            self._words = self._words + action.replace

        for action in new:
            remove = len(action.replace)
            if remove > 0:
                self._words = self._words[:-remove]
            self._words = self._words + action.text

        # Limit phrasing memory to 100 characters, because most phrases probably
        # don't exceed this length
        self._words = self._words[-100:]

        split_words = self.WORDS_RX.findall(self._words)
### end abfridged snippet of Suggestions dialogue code    
        self.last_individual_words = split_words

    def get_last(self, previous_count):
        return self.last_individual_words[-previous_count:]

previous_translations = PreviousTranslations()

def init_context_aware(engine, cmdline):
    engine.signal_connect('translated', previous_translations.on_translation)

def launch_in_bg(engine, cmdline):
    if "$$LAST_STROKE" in cmdline:
        last_stroke_list = previous_translations.get_last(1)
        last_stroke = last_stroke_list[0] if last_stroke_list else ""
        cmdline = cmdline.replace("$$LAST_STROKE", last_stroke)
    print(">> ", cmdline)
    subprocess.Popen(cmdline, shell=True)
     
def print_last_words(engine, cmdline):
    previous_count = int(cmdline)
    print(previous_count)
    print(previous_translations.get_last(previous_count))
