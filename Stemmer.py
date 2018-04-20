from nltk.stem.porter import *
import re
import pprint
import string

comments = []
'''
Parses test and gets comments between /** and */, stripping out asterisks and tabs
'''
def getComments(text):
    for comment in re.findall(r'\*\*(.*?)\*\/', text, re.S):
        cleaned = re.sub('\n+', ',', re.sub(r'[ *]+', ' ', comment.strip()).strip())
        comments.append(re.sub(' +', ' ', cleaned.translate(string.maketrans("\t", " "))))

# TEST READ IN JAVA AND GET COMMENTS
with open('PartServiceImpl.txt', 'r') as myfile:
    rawText = myfile.read()
getComments(rawText)
pprint.pprint(comments)

# TEST PORTER STEMMER
stemmer = PorterStemmer()
sampleWords = ['ElementTreeSelectionDialog', 'ProgressInfoItem', 'DelegatingStyledCellLabelProvider']
stemmedWords = dict.fromkeys(sampleWords, [])

for word in stemmedWords:
    stemmedWords[word] = [stemmer.stem(base) for base in re.sub(r"([A-Z])", r" \1", word).split()]

pprint.pprint(stemmedWords)