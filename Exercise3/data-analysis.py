import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from nltk.corpus import gutenberg

# Download the necessary data 
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('gutenberg')
nltk.download('vader_lexicon')

# Read the Moby Dick file from the Gutenberg dataset
moby_dick_text = gutenberg.raw('melville-moby_dick.txt')

# Tokenization
tokens = word_tokenize(moby_dick_text)

# Stop-words filtering
stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

# Parts-of-Speech (POS) tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# POS frequency
pos_freq = nltk.FreqDist(tag for (word, tag) in pos_tags)
top_pos_freq = pos_freq.most_common(5)
print(top_pos_freq)
print('The 5 most common parts of speech and their frequency ：')
for pos, freq in top_pos_freq:
    print(pos, ':', freq)

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(token) for (token, pos) in pos_tags[:20]]
print('The top 20 tokens lemmatized：')
for token in lemmatized_tokens:
    print(token)

# Plotting frequency distribution
pos_labels = [tag for (tag, count) in top_pos_freq]
pos_counts = [count for (tag, count) in top_pos_freq]
plt.bar(pos_labels, pos_counts)
plt.title('The frequency of POS')
plt.xlabel('Parts of speech')
plt.ylabel('Total occurrences')
plt.show()

# Sentiment analysis
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = [analyzer.polarity_scores(token)['compound'] for token in tokens]
average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
print('The average sentiment score :', average_sentiment)


# Judge the overall text sentiment 
if average_sentiment > 0.05:
    print('The overall text sentiment is positive')
else:
    print('The overall text sentiment is negative')

    