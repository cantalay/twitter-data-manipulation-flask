from flask import Flask, render_template, request
from twython import Twython
import numpy as np
import re
from collections import Counter,OrderedDict
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

app = Flask(__name__)

APP_KEY =
ACCESS_TOKEN = 
APP_SECRET = 
OAUTH_TOKEN = 
OAUTH_TOKEN_SECRET = 
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

@app.route('/',  methods=['GET', 'POST'])
def hello_world():
    post = request.form.get('selectData')
    if post == None:
        post = "Zeytin Dalı"
    print(post)

    wordnum = []
    allWord = []
    tweet4tfidf = []


    query = post + ' AND -filter:retweets AND -filter:replies'
    try:
        results = twitter.cursor(twitter.search, q=query, count=100)
        for result in results:
                lowercase = result['text'].lower()
                print(lowercase)
                word = word2 = re.sub('http://\S+|https://\S+', '', lowercase)
                tweet4tfidf.append(word)
                tweetList = changeTweet(lowercase)
                wordnum.append(len(tweetList))
                allWord += tweetList

    except StopIteration as e:
        print(e)
    except:
        print("HATAAAAAA")
    tfidfAnalyse(tweet4tfidf)
    for x,y in mostCommon(allWord):
        print(x,"--",y)
    frequent = mostCommon(allWord)
    print("Most Frequently : ", mostCommon(allWord))
    print("Word num : ", wordnum)
    print("all Word: ", allWord)
    print("Average : ", np.mean(wordnum))
    print(np.mean(wordnum))

    return render_template(
        'index.html',
        frequent=frequent,
        average=np.mean(wordnum),
        significant=tfidfAnalyse(tweet4tfidf),
        post=post)


def changeTweet(word):
    word = word.replace(".", "")
    word = word.replace(",", "")
    word = word.replace("'", "")
    word = word.replace(":", "")
    word = word.replace("\"", "")
    word = word.replace("!", "")
    word = word.replace("#", "")
    word = word.replace("*", "")
    word = word.replace("\n", " ")
    word = word.split()
    return word


def mostCommon(allWord):
    counter = Counter(allWord)
    mostOccur = counter.most_common(20)
    return mostOccur


def tfidfAnalyse(tweet):
    cv = CountVectorizer()
    data = cv.fit_transform(tweet)
    tfidf_transformer = TfidfTransformer()
    tfidf_matrix = tfidf_transformer.fit_transform(data)
    word2tfidf = dict(zip(cv.get_feature_names(), tfidf_transformer.idf_))
    sorteddict = sorted(word2tfidf.items(), key=lambda kv: kv[1], reverse=True)
    print("SORT",sorteddict)
    return sorteddict



if __name__ == '__main__':
    app.run()
