#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
import music21


def get_top_line(piece):
    top_part = piece.parts[0]

    # replace all chords with top note of chord
    for item in top_part.notes:
        if isinstance(item, music21.chord.Chord):
            top_part.notes.replace(item, item[0])
    return top_part


def write_files(piece_obj, composer, piece_name, output_dir="data/preprocessed"):
    output_dir = os.path.join(output_dir, composer)

    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass


    top_line = get_top_line(piece_obj)

    # create measures
    top_line.makeMeasures(inPlace=True)

    counter = 1
    while True:
        # currently hardcoded for 2 measures. generalize?
        measure_num = 2*counter - 1
        section = top_line.measures(measure_num, measure_num + 1)

        if len(section) == 0:
            # Reached the end of the piece
            break

        filename = os.path.join(output_dir, "%s_%03d.xml" % (piece_name, counter))
        section.write(fmt="musicxml", fp=filename)

        counter += 1


def run():
    preprocessed_dir = "data/preprocessed"
    raw_dir = "data/raw"
    composers = os.listdir(raw_dir)

    # If preprocessed directory exists, ask user to confirm removing the directory
    if os.path.exists(preprocessed_dir):
        print("Directory \"%s\" exists. Remove? [y/N]")
        answer = input()
        if len(answer) == 0 or answer[0].lower() != "y":
            sys.exit()

        # Confirmed
        shutil.rmtree(preprocessed_dir)


    for composer in composers:
        composer_dir = os.path.join(raw_dir, composer)
        pieces = os.listdir(composer_dir)

        for piece_name in pieces:
            filename = os.path.join(composer_dir, piece_name)
            print("Reading: %s" % filename)
            piece_obj = music21.converter.parse(filename)

            # Create a friendly piece name (w/o file extension)
            friendly_piece_name = os.path.splitext(piece_name)[0]

            write_files(piece_obj, composer=composer, piece_name=friendly_piece_name)


def main():
    description = ("Split each data file into multiple melodic examples"
                   " and ouptut them as MusicXML files")
    parser = argparse.ArgumentParser(__file__, description=description)
    args = parser.parse_args()
    run()


if __name__ == "__main__":
    main()
