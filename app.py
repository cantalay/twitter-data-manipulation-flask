from flask import Flask, render_template, request
from twython import Twython
import numpy as np
from string import digits
import re
from collections import Counter,OrderedDict
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

app = Flask(__name__)

APP_KEY = "Xvgpb18d4pJNBwSJaJ0JhkUPn"
ACCESS_TOKEN = "1370537623-Brb7RYIklcMKrRcNYbMq1alWZK8WtXy7uaDmLul"
APP_SECRET = "7ihL6R70skJywPDWaFk8lsjIEY6NsYbIZIgkhD6ogdyBFkvjix"
OAUTH_TOKEN = "1370537623-Brb7RYIklcMKrRcNYbMq1alWZK8WtXy7uaDmLul"
OAUTH_TOKEN_SECRET = "D4kfNfIcD36vkqa9mp0sy75K61AcOmcXZvdJPh09OFzKZ"
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
@app.route('/',  methods=['GET', 'POST'])
def twitterApi():
    post = request.form.get('selectData')
    if post == None:
        post = "Zeytin Dalı"
    print("Search Keyword",post)

    wordnum = []
    allWord = []
    tweet4tfidf = []

    x = 0
    query = post + ' AND -filter:retweets'
    try:
        results = twitter.cursor(twitter.search, q=query)
        for result in results:
            x+=1
            lowercase = result['text'].lower()
            word = re.sub('http://\S+|https://\S+', '', lowercase)
            removedigit = str.maketrans('', '', digits)
            word = word.translate(removedigit)
            tweet4tfidf.append(word)
            tweetList = changeTweet(word)
            wordnum.append(len(tweetList))
            allWord += tweetList

    except StopIteration as e:
        print(e)
    except:
        print("Other Itteration Error")

    print("TFIDF TWEET",tweet4tfidf)
    if not tweet4tfidf == []:
        tfidfAnalyse(tweet4tfidf)
    frequent = mostCommon(allWord)

    return render_template(
        'index.html',
        frequent=frequent,
        average=np.mean(wordnum),
        significant=tfidfAnalyse(tweet4tfidf),
        countedTweet = x,
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
    sorteddict = sorted(word2tfidf.items(), key=lambda x: x[1], reverse=True)
    return sorteddict



if __name__ == '__main__':
    app.run()
