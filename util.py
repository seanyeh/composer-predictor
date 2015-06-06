#!/usr/bin/env python3

import operator
from functools import reduce

import music21


def get_top_line(piece):
    top_part = piece.parts[0]
    if len(top_part.voices) > 0:
        top_part = top_part.voices[0]

    # replace all chords with top note of chord
    for item in top_part.notes:
        if isinstance(item, music21.chord.Chord):
            top_part.notes.replace(item, item[0])
    return top_part


def get_notes(piece):
    part = piece.parts[0]
    measures = filter(lambda x: isinstance(x, music21.stream.Measure), part.elements)

    # add all the notes from all the measures
    notes = reduce(operator.add, map(lambda x: x.notes.elements, measures))

    return list(notes)

