#!/usr/bin/env python3

import argparse
import os
import music21
import pandas

import features as features_lib

# All functions (excluding those starting with _) are feature functions
def get_features():

    # Hey look, it's a smiley face --------
    #                                     |
    #                                     v

    return list(filter(lambda x: x[0] != "_", dir(features_lib)))


def split_arr(arr, ratio=0.7):
    index = int(len(arr) * ratio)
    return arr[:index], arr[index:]


def generate_dataframes(preprocessed_dir):
    composers = os.listdir(preprocessed_dir)

    feature_names = get_features()
    examples_train = []
    examples_test = []
    for composer in composers:
        examples_temp = []
        composer_dir = os.path.join(preprocessed_dir, composer)
        pieces = os.listdir(composer_dir)

        for piece_name in pieces:
            filename = os.path.join(composer_dir, piece_name)
            piece_obj = music21.converter.parse(filename)
            item = {"composer": composer, "filename": piece_name}

            for feature in feature_names:
                feature_func = getattr(features_lib, feature)
                item[feature] = feature_func(piece_obj)

            examples_temp.append(item)

        # Split examples_temp into training and testing set
        temp1, temp2 = split_arr(examples_temp)
        examples_train += temp1
        examples_test += temp2


    return pandas.DataFrame(examples_train), pandas.DataFrame(examples_test)


def run(output_dir, input_dir):
    df_train, df_test = generate_dataframes(preprocessed_dir=input_dir)

    # write them to csv
    filename = os.path.join(output_dir, "data_%s.csv")
    df_train.to_csv(filename % "train")
    df_test.to_csv(filename % "test")


def main():
    description = ("Read in MusicXML files, apply features to each example,"
                   " and output training and testing datasets as CSV files")
    parser = argparse.ArgumentParser(__file__, description=description)

    args = parser.parse_args()

    run(output_dir="data", input_dir="data/preprocessed")


if __name__ == "__main__":
    main()
