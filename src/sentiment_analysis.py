import csv

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

from utils.paths import get_data_path

NEGATIVE = 'neg'
POSITIVE = 'pos'
NEUTRAL = 'neu'
UNKNOWN = 'unk'


def word_feats(words):
    return dict([(word, True) for word in words])


def test_classifier(classifier_, tweets):
    for tweet in tweets:
        corpus = word_feats(tweet[headers.index('text')].split(' '))
        print(': ' + classifier_.classify(corpus))


if __name__ == '__main__':
    neg_ids = movie_reviews.fileids(NEGATIVE)
    pos_ids = movie_reviews.fileids(POSITIVE)

    neg_feats = [(word_feats(movie_reviews.words(fileids=[f])), NEGATIVE) for f in neg_ids]
    pos_feats = [(word_feats(movie_reviews.words(fileids=[f])), POSITIVE) for f in pos_ids]

    neg_cutoff = round(len(neg_feats) * 3 / 4)
    pos_cutoff = round(len(pos_feats) * 3 / 4)

    train_feats = neg_feats[:neg_cutoff] + pos_feats[:pos_cutoff]
    # test_feats = neg_feats[neg_cutoff:] + pos_feats[pos_cutoff:]
    #
    # print('train on %d instances, test on %d instances' % (len(train_feats), len(test_feats)))
    #
    classifier = NaiveBayesClassifier.train(train_feats)
    # print('accuracy: ', nltk.classify.util.accuracy(classifier, test_feats))

    ##########################################

    with open(get_data_path() + '/tweets.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        tweets_for_test = [row for row in csv_reader]
        headers = tweets_for_test.pop(0)

    test_data = [(word_feats(tweet[headers.index('text')].split(' ')), UNKNOWN) for tweet in tweets_for_test]
    test_classifier(classifier, tweets_for_test)

    classifier.show_most_informative_features()

    print(len(tweets_for_test))
