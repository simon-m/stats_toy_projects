from __future__ import division

import os
import sys
import re
import random

from numpy.random import choice
from numpy import empty

class Text_markov_model(object):
    def __init__(self, order=1):
        self.order = order
        self.prefix_to_suffix_proba = {}
        self.prefix_counts = {}

    def feed_training_set(self, fpath_or_string):
        if not os.path.isfile(fpath_or_string):
            sys.stderr.write("Text_markov_model::feed_traning_set() warning: Intepreting argument as string instead of file path\n")
            text = re.sub("\s+", " ", fpath_or_string.strip().replace("\n", " ")).lower().split(" ")
            self._update_prefix_to_suffix_proba(text, [])
        else:
            with open(fpath_or_string) as fh:
                previous_line_elts = []
                for line in fh:
                    line = line.strip()
                    if line == "":
                        continue
                    elts = re.sub("\s+", " ", line).lower().split(" ")
                    self._update_prefix_to_suffix_proba(elts, previous_line_elts)
                    previous_line_elts = elts
                    
    def _update_prefix_to_suffix_proba(self, elts, p_elts):
        for i in range(len(elts)):
            p_elts_prefix_min = max(0, len(p_elts) - self.order + i)
            p_elts_prefix_max = len(p_elts)
            elts_prefix_min = max(0, i - self.order)
            elts_prefix_max = i

            p_elts_prefix = [p_elts[j] for j in range(p_elts_prefix_min, p_elts_prefix_max)]
            elts_prefix = [elts[j] for j in range(elts_prefix_min, elts_prefix_max)]
            pre_prefix = p_elts_prefix + elts_prefix
            prefix = tuple(["" for j in range(self.order - len(pre_prefix))] + pre_prefix)

            if not prefix in self.prefix_counts:
                self.prefix_counts[prefix] = 0
            self.prefix_counts[prefix] += 1

            suffix = elts[i]
            if not prefix in self.prefix_to_suffix_proba:
                self.prefix_to_suffix_proba[prefix] = {}
            if not suffix in self.prefix_to_suffix_proba[prefix]:
                self.prefix_to_suffix_proba[prefix][suffix] = 0
            self.prefix_to_suffix_proba[prefix][suffix] += 1

    def get_most_likely_suffix(self, prefix):
        padded_prefix = tuple(["" for i in range(self.order - len(prefix))] + prefix)
        max_suffix = ""
        max_count = 0
        if not padded_prefix in self.prefix_to_suffix_proba:
            return ""

        for suffix in self.prefix_to_suffix_proba[padded_prefix]:
            if self.prefix_to_suffix_proba[padded_prefix][suffix] > max_count:
                max_count = self.prefix_to_suffix_proba[padded_prefix][suffix]
                max_suffix = suffix
        return max_suffix

    def get_random_suffix(self, prefix):
        padded_prefix = tuple(["" for i in range(self.order - len(prefix))] + prefix)
        suffixes = []
        probas = []
        if not padded_prefix in self.prefix_to_suffix_proba:
            return ""

        for suffix in self.prefix_to_suffix_proba[padded_prefix]:
            suffixes.append(suffix)
            probas.append(self.prefix_to_suffix_proba[padded_prefix][suffix] / self.prefix_counts[padded_prefix])
        return choice(suffixes, p=probas)

    def get_sentence(self, prefix, draw_function, max_len=100):            
        suffix = None
        sentence = []
        i = 0
        while suffix != "" and i < max_len:
            suffix = draw_function(prefix)
            sentence.append(suffix)
            prefix = [prefix[j] for j in range(1, len(prefix))] + [suffix]
            i += 1
        return " ".join(sentence)

    def get_most_likely_sentence(self, prefix, max_len=sys.maxint):
        return self.get_sentence(prefix, self.get_most_likely_suffix, max_len)

    def get_random_sentence(self, prefix, max_len=sys.maxint):
        return self.get_sentence(prefix, self.get_random_suffix, max_len)

                
tmm = Text_markov_model(4)
for fpath in sorted(filter(lambda x: x[-4:] == ".txt", os.listdir("."))):
    print(fpath)
    tmm.feed_training_set(fpath)

# tmm.feed_training_set("a b c d e f g a b f e d g f f e s g b b g e s s  a a f g g f f a e f g")
#
pc_list = [(tmm.prefix_counts[pref], pref) for pref in tmm.prefix_counts]
spc_list = sorted(pc_list, key=lambda x: x[0], reverse=True)

# for pref in tmm.prefix_to_suffix_proba:
#     print(pref)
#     print(tmm.prefix_to_suffix_proba[pref])
#    print("")

# mprefix_txt = "one of the"
# mprefix = mprefix_txt.split(" ")
mprefix = list(spc_list[random.randint(0, len(spc_list))][1])
# print(tmm.get_most_likely_suffix(mprefix))
# print(tmm.get_random_suffix(mprefix))

print(" ".join(mprefix) + " " + tmm.get_most_likely_sentence(mprefix, 100))
print(" ".join(mprefix) + " " + tmm.get_random_sentence(mprefix, 1000))

    
    
                    
                    
                    
