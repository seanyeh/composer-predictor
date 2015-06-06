#!/usr/bin/env python3

import inspect
import operator
import sys

from functools import reduce


import music21

'''
Write all your feature-evaluating functions in this file.

# All helper functions begin with an underscore
def _favorite_helper():
    return 1

# All other functions will be recognized as a feature function
# Feature functions will take a music21 piece object as its argument
def my_favorite_feature(piece):
    return _helper()

'''

def _get_notes(piece):
    part = piece.parts[0]
    measures = filter(lambda x: isinstance(x, music21.stream.Measure), part.elements)

    # add all the notes from all the measures
    notes = reduce(operator.add, map(lambda x: x.notes, measures))

    return list(notes)


def num_notes(piece):
    return len(_get_notes(piece))



'''
Create list of features
    (must stay at bottom of file)
'''
def _get_functions(module):
    # getmembers returns list of tuples (func_name, func)
    members = filter(lambda x: inspect.isfunction(x[1]) and x[0][0] != "_",
                     inspect.getmembers(module))

    # only return names
    return list(map(lambda x: x[0], members))

FEATURES = _get_functions(sys.modules[__name__])
