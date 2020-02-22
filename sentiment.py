import pandas as pd
from sklearn.utils import shuffle
df = pd.read_csv('drive/My Drive/dataset/training.1600000.processed.noemoticon.csv',encoding="ISO-8859-1")
df = df.iloc[:,[5,0]]
df = shuffle(df)
df.columns = ['tweet','sentiment']

import numpy as np
dataset = df.iloc[:150000,:]
print(np.shape(dataset))
df1 = df.tail(150000)
print(np.shape(df1))


dataset = dataset.append(df1,ignore_index=True)

print(np.shape(dataset))
print(dataset.head())
print(dataset.tail())

import re
import numpy as np


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt


import re
import numpy as np


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt
dataset['tidy_tweet'] = dataset['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
dataset['tidy_tweet'].head()

dataset['tidy_tweet'] = dataset['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
dataset['tidy_tweet'].head()

dataset['tidy_tweet'] = dataset['tidy_tweet'].str.lower()
dataset['tidy_tweet'].head()

tokenized_tweet = dataset['tidy_tweet'].apply(lambda x: x.split())
tokenized_tweet.head()

from nltk.stem.porter import *
stemmer = PorterStemmer()

tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming
tokenized_tweet.head()

for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

dataset['tidy_tweet'] = tokenized_tweet

import matplotlib.pyplot as plt
all_words = ' '.join([text for text in dataset['tidy_tweet']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

positive_words =' '.join([text for text in dataset['tidy_tweet'][dataset['sentiment'] == 4]])

wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(positive_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

negative_words = ' '.join([text for text in dataset['tidy_tweet'][dataset['sentiment'] == 0]])
wordcloud = WordCloud(width=800, height=500,
random_state=21, max_font_size=110).generate(negative_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# function to collect hashtags
def hashtag_extract(x):
    hashtags = []
    # Loop over the words in the tweet
    for i in x:
        ht = re.findall(r"#(\w+)", i)
        hashtags.append(ht)

    return hashtags
HT_regular = hashtag_extract(dataset['tidy_tweet'][dataset['sentiment'] == 4])





HT_negative = hashtag_extract(dataset['tidy_tweet'][dataset['sentiment'] == 0])

# unnesting list
HT_regular = sum(HT_regular,[])
HT_negative = sum(HT_negative,[])

import nltk
import seaborn as sns
import matplotlib as plt
a = nltk.FreqDist(HT_regular)
d = pd.DataFrame({'Hashtag': list(a.keys()),
                  'Count': list(a.values())})

# selecting top 10 most frequent hashtags
d = d.nlargest(columns="Count", n = 10)
plt.figure(figsize=(16,5))
ax = sns.barplot(data=d, x= "Hashtag", y = "Count")
plt.show()

b = nltk.FreqDist(HT_negative)
e = pd.DataFrame({'Hashtag': list(b.keys()), 'Count': list(b.values())})
# selecting top 10 most frequent hashtags
e = e.nlargest(columns="Count", n = 10)
plt.figure(figsize=(16,5))
ax = sns.barplot(data=e, x= "Hashtag", y = "Count")
plt.show()

from sklearn.feature_extraction.text import CountVectorizer
bow_vectorizer = CountVectorizer(max_df=0.90, min_df=1, max_features=6000, stop_words='english')
# bag-of-words feature matrix
bow = bow_vectorizer.fit_transform(dataset['tidy_tweet'])
print(bow.toarray()[0:5])
print(bow_vectorizer.get_feature_names()[0:20])

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# splitting data into training and test set
xtrain_bow, xtest_bow, ytrain, ytest = train_test_split(bow, dataset['sentiment'], random_state=42, test_size=0.3)

lreg = LogisticRegression()
lreg.fit(xtrain_bow, ytrain) # training the model
model = lreg
prediction = lreg.predict(xtest_bow)
cm = confusion_matrix(ytest,prediction)
print(cm)
accuracy = ((cm[0][0]+cm[1][1])/(sum(sum(cm))))*100
print("accuracy = ",accuracy)

text = "what an amazing & fantastic day today"
text = text.split()
bow_real = bow_vectorizer.fit(text)
print(bow_real.toarray()[0:5])
prediction = lreg.predict(bow_real)

from sklearn.externals import joblib
filename = 'finalized_model.sav'
joblib.dump(model, filename)

# load the model from disk
# loaded_model = joblib.load(filename)
# result = loaded_model.score(X_test, Y_test)
# print(result)

def predictAnalysis(realTweets):
    loaded_model = joblib.load(filename)
    result = loaded_model.predict(realTweets)
    return result