from nltk.stem.porter import *
import re
import pprint

stemmer = PorterStemmer()
sampleWords = ['ElementTreeSelectionDialog', 'ProgressInfoItem', 'DelegatingStyledCellLabelProvider']

stemmedWords = dict.fromkeys(sampleWords, [])

for word in stemmedWords:
    stemmedWords[word] = [stemmer.stem(base) for base in re.sub(r"([A-Z])", r" \1", word).split()]

pprint.pprint(stemmedWords)