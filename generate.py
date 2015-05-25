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


def generate_dataframe(preprocessed_dir):
    composers = os.listdir(preprocessed_dir)

    feature_names = get_features()
    examples = []
    for composer in composers:
        composer_dir = os.path.join(preprocessed_dir, composer)
        pieces = os.listdir(composer_dir)

        for piece_name in pieces:
            filename = os.path.join(composer_dir, piece_name)
            piece_obj = music21.converter.parse(filename)
            item = {"composer": composer, "filename": piece_name}

            for feature in feature_names:
                feature_func = getattr(features_lib, feature)
                item[feature] = feature_func(piece_obj)

            examples.append(item)

    return pandas.DataFrame(examples)


def run(output_dir, input_dir):
    df = generate_dataframe(preprocessed_dir=input_dir)

    rows = len(df)

    # TODO: split into training and testing sets for each composer.
    #
    # df.to_csv(output_file)


def main():
    description = ("Read in MusicXML files, apply features to each example,"
                   " and output training and testing datasets as CSV files")
    parser = argparse.ArgumentParser(__file__, description=description)

    args = parser.parse_args()

    run(output_dir="data", input_dir="data/preprocessed")


if __name__ == "__main__":
    main()
