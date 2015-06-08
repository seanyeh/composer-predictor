#!/usr/bin/env python3

import argparse

import numpy
import pandas

from sklearn import svm, cross_validation

import features



def load_XY(filename):
    df = pandas.read_csv(filename)
    return df[features.FEATURES].values, df.composer.values


def test(x_train, y_train, x_test, y_test):
    clf = svm.SVC().fit(x_train, y_train)
    return clf.score(x_test, y_test)


def cross_validate(x, y):
    return cross_validation.cross_val_score(svm.SVC(), x, y, cv=5)





def main():
    parser = argparse.ArgumentParser(__file__)

    parser.add_argument("--train-data", metavar="TRAIN_DATA",
                        nargs="?", default="data/data_train.csv",
                        help="Filename of training data (csv format)")

    parser.add_argument("--test-data", metavar="TEST_DATA",
                        nargs="?", default="data/data_test.csv",
                        help="Filename of testing data (csv format)")

    parser.add_argument("-t", "--test", action="store_true",
                        help="Show prediction accuracy on test data")

    parser.add_argument("-c", "--cross-validate", action="store_true",
                        help="Print cross-validation scores")

    args = parser.parse_args()


    x_train, y_train = load_XY(args.train_data)
    x_test, y_test = load_XY(args.test_data)
    if args.cross_validate:
        scores = cross_validate(x_train, y_train)
        print("Cross-validation scores:", scores)
        print("Cross-validation avg:", numpy.mean(scores))

    if args.test:
        print("Prediction accuracy on test data:",
              test(x_train, y_train, x_test, y_test))



if __name__ == "__main__":
    main()
