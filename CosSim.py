# Code written by Nasir Safdari
from nltk.tokenize import  word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
words = stopwords.words("english")
# stemming and tokenizing
def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens if item not in words]

# remove punctuation, lowercase, stem
def normalize(text):
    return stem_tokens(word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, min_df = 1, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]