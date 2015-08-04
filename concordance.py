__author__ = 'Darthfrazier'

import re

dict = {}
abbreviations = {'dr.': 'doctor', 'mr.': 'mister', 'bro.': 'brother', 'bro': 'brother', 'mrs.': 'mistress', 'ms.': 'miss', 'jr.': 'junior', 'sr.': 'senior',
                 'i.e.': 'for example', 'e.g.': 'for example', 'vs.': 'versus'}
terminators = ['.', '!', '?']
wrappers = ['"', "'", ')', ']', '}']

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def find_sentences(paragraph):
    end = True
    sentences = []
    while end > -1:
        end = find_sentence_end(paragraph)
        if end > -1:
            sentences.append(paragraph[end:].strip())
            paragraph = paragraph[:end]
    sentences.append(paragraph)
    sentences.reverse()
    return sentences


def find_sentence_end(paragraph):
    [possible_endings, contraction_locations] = [[], []]
    contractions = abbreviations.keys()
    sentence_terminators = terminators + [terminator + wrapper for wrapper in wrappers for terminator in terminators]

    for sentence_terminator in sentence_terminators:
        t_indices = list(find_all(paragraph, sentence_terminator))
        possible_endings.extend(([] if not len(t_indices) else [[i, len(sentence_terminator)] for i in t_indices]))

    for contraction in contractions:
        c_indices = list(find_all(paragraph, contraction))
        contraction_locations.extend(([] if not len(c_indices) else [i + len(contraction) for i in c_indices]))
    possible_endings = [pe for pe in possible_endings if pe[0] + pe[1] not in contraction_locations]

    if len(paragraph) in [pe[0] + pe[1] for pe in possible_endings]:
        max_end_start = max([pe[0] for pe in possible_endings])
        possible_endings = [pe for pe in possible_endings if pe[0] != max_end_start]
    possible_endings = [pe[0] + pe[1] for pe in possible_endings if sum(pe) > len(paragraph) or (sum(pe) < len(paragraph) and paragraph[sum(pe)] == ' ')]
    end = (-1 if not len(possible_endings) else max(possible_endings))
    return end

def concordance(tokens):

    for i in range(0, len(tokens)):
        text = tokens[i]
        text = re.sub('[^a-z\ \']+', " ", text)
        for word in text.split():
            if not word in dict:
                dict[word] = [i]
            else:
                templist = dict[word]
                templist.append(i)

def main():
    text = ""
    stopword = ""

    while True:
        line = raw_input("Input text for Concordance: ")
        line = line.lower()
        if line.strip() == stopword:
            break
        text += "%s\n" % line

    tokens = find_sentences(text)

    #tokens = tokenize.sent_tokenize(text)
    #text = "HELLO TWO WHAT A LOST CAUSE. HELLO. HELLO YOU TWO A HOLES"
    concordance(tokens)

    print "%-15s %-10s %s" %("Word", "Frequency", "Index of Occurrence")
    print "-"*50
    for key in sorted(dict):
        temp = str(dict[key])
        print "%-15s: %-10d %-15s" %(str(key), len(dict[key]), temp)

if __name__ == '__main__':
    main()