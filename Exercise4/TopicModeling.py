import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import pyLDAvis.gensim

# Load Alice's Adventures in Wonderland text 
nltk.download('gutenberg')
alice = gutenberg.sents('carroll-alice.txt')

# Participle and stop word removal 
stop_words = set(stopwords.words('english'))
texts = [[word.lower() for word in sentence if word.isalpha() and word.lower() not in stop_words] for sentence in alice]

# Building a dictionary 
dictionary = corpora.Dictionary(texts)

# Building document-word frequency matrix 
corpus = [dictionary.doc2bow(text) for text in texts]

# Thematic modeling using LDA 
lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10)

# Visual themes 
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis)
