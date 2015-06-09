#!/usr/bin/env python3

import argparse
import sys

import numpy
import pandas

from sklearn import svm, cross_validation, ensemble

import features


AVAILABLE_ALGORITHMS = {
        "ExtraTreesClassifier":
            lambda:ensemble.ExtraTreesClassifier(n_estimators=250, random_state=0),
        "SVC": svm.SVC
}


def load_XY(filename, features_list):
    df = pandas.read_csv(filename)
    return df[features_list].values, df.composer.values


def test(algorithm, x_train, y_train, x_test, y_test):
    clf = algorithm().fit(x_train, y_train)
    score = clf.score(x_test, y_test)

    print("\nPrediction accuracy on test data:", score)


def cross_validate(algorithm, x, y):
    scores = cross_validation.cross_val_score(algorithm(), x, y, cv=5)
    print("\nCross-validation scores:", scores)
    print("Cross-validation avg:", numpy.mean(scores))


def show_feature_importances(x, y, features_list):
    print("\nFeature Importances:")
    forest = ensemble.ExtraTreesClassifier(n_estimators=250, random_state=0)
    forest.fit(x, y)

    importances = list(zip(forest.feature_importances_, features_list))
    # sort in place
    importances.sort(key=lambda x: x[0], reverse=True)
    for tup in importances:
        print("%f: %s" % tup)





def main():
    parser = argparse.ArgumentParser(__file__)

    parser.add_argument("--train-data", metavar="TRAIN_DATA",
                        nargs="?", default="data/data_train.csv",
                        help="Filename of training data (csv format)")

    parser.add_argument("--test-data", metavar="TEST_DATA",
                        nargs="?", default="data/data_test.csv",
                        help="Filename of testing data (csv format)")

    parser.add_argument("--algorithm", metavar="TEST_DATA",
                        nargs="?", default="ExtraTreesClassifier",
                        help=("Name of algorithm to use. Available:"
                        ",".join(AVAILABLE_ALGORITHMS.keys()) + ""
                        " Default: ExtraTreesClassifier"))

    parser.add_argument("-i", "--ignore-features", type=lambda x:x.split(","),
                        nargs="?", default=[],
                        help="Comma-separated list of features to ignore")

    parser.add_argument("-t", "--test", action="store_true",
                        help="Show prediction accuracy on test data")

    parser.add_argument("-c", "--cross-validate", action="store_true",
                        help="Print cross-validation scores")

    parser.add_argument("-f", "--feature-importances", action="store_true",
                        help="Show feature importances")

    args = parser.parse_args()


    features_list = [x for x in features.FEATURES if x not in args.ignore_features]

    x_train, y_train = load_XY(args.train_data, features_list)
    x_test, y_test = load_XY(args.test_data, features_list)

    if args.algorithm not in AVAILABLE_ALGORITHMS:
        print("Algorithm \"%s\" not available." % args.algorithm)
        sys.exit(1)
    algorithm = AVAILABLE_ALGORITHMS[args.algorithm]

    if args.cross_validate:
        cross_validate(algorithm, x_train, y_train)

    if args.test:
        test(algorithm, x_train, y_train, x_test, y_test)

    if args.feature_importances:
        show_feature_importances(x_train, y_train, features_list)



if __name__ == "__main__":
    main()
