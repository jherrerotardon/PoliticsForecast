import csv

from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
import re

from utils.paths import get_data_path

NEGATIVE = 'negative'
POSITIVE = 'positive'
NEUTRAL = 'neutral'
UNKNOWN = 'unk'

stopwords_list = set(stopwords.words('english'))


def tokenize_clean_text(text) -> list:
    text = re.sub(r"https?\S+", "", text)
    text = re.sub(r"@\S+", "", text)

    text = text.lower()

    # Remove punctuation.
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(text)

    # Not remove punctuation.
    # word_tokens2 = word_tokenize(text)

    return [w for w in word_tokens if w not in stopwords_list]


def word_feats(words):
    return dict([(word, True) for word in words])


def test_classifier(classifier_, tweets):
    result_ = {
        POSITIVE: 0,
        NEUTRAL: 0,
        NEGATIVE: 0,
    }

    with open(get_data_path() + '/result.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for tweet in tweets:
            corpus = word_feats(tokenize_clean_text(tweet[headers.index('text')]))
            sentiment = classifier_.classify(corpus)
            result_[sentiment] += 1

            writer.writerow([tweet[headers.index('text')], sentiment])

    return result_


def read_csv(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows_ = [row for row in csv_reader]
        headers_ = rows_.pop(0)

    return headers_, rows_


if __name__ == '__main__':
    headers, train_data = read_csv(get_data_path() + '/reviews.csv')

    neg_feats = [(word_feats(tokenize_clean_text(tweet[headers.index('text')])), NEGATIVE) for tweet in train_data if
                 tweet[headers.index('airline_sentiment')] == NEGATIVE]
    pos_feats = [(word_feats(tokenize_clean_text(tweet[headers.index('text')])), POSITIVE) for tweet in train_data if
                 tweet[headers.index('airline_sentiment')] == POSITIVE]
    neu_feats = [(word_feats(tokenize_clean_text(tweet[headers.index('text')])), NEUTRAL) for tweet in train_data if
                 tweet[headers.index('airline_sentiment')] == NEUTRAL]

    neg_cutoff = round(len(neg_feats) * 3 / 4)
    pos_cutoff = round(len(pos_feats) * 3 / 4)
    neu_cutoff = round(len(neu_feats) * 3 / 4)

    train_feats = neg_feats[:neg_cutoff] + pos_feats[:pos_cutoff] + neu_feats[:neu_cutoff]
    test_feats = neg_feats[neg_cutoff:] + pos_feats[pos_cutoff:] + neu_feats[neu_cutoff:]

    # Train Classifier.
    print('train on %d instances, test on %d instances' % (len(train_feats), len(test_feats)))
    classifier = NaiveBayesClassifier.train(train_feats)
    print('accuracy: ', accuracy(classifier, test_feats))

    # Get data to test.
    headers, tweets_for_test = read_csv(get_data_path() + '/tweets.csv')
    test_data = [(word_feats(tokenize_clean_text(tweet[headers.index('text')])), UNKNOWN) for tweet in tweets_for_test]
    result = test_classifier(classifier, tweets_for_test)

    print('There are ' + str(result[NEGATIVE]) + ' negatives tweets.')
    print('There are ' + str(result[POSITIVE]) + ' positives tweets.')
    print('There are ' + str(result[NEUTRAL]) + ' neutrals tweets.')

    classifier.show_most_informative_features()
