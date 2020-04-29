from collections import defaultdict
import ujson
from heapq import nlargest
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')


def open_json_file(file_loc):
    if file_loc:
        with open(file_loc, 'r') as file:
            return ujson.loads(file.read())


customStopWords = set(stopwords.words('english')+list(punctuation)+['\n'])


def summarize(text, num_of_sentences=5):
    word_sent = word_tokenize(text.lower())
    wordsWOStopwords = [
        word for word in word_sent if word not in customStopWords]
    freq = FreqDist(wordsWOStopwords)
    sents = sent_tokenize(text)
    ranking = defaultdict(int)
    for i, sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]
    sents_idx = nlargest(num_of_sentences, ranking, key=ranking.get)
    summary_statement_list = []
    for each in [sents[j] for j in sorted(sents_idx)]:
        summary_statement_list.append(each)
    return summary_statement_list
