#!/usr/bin/env python3

import inspect
import operator
import sys

from functools import reduce

import numpy
import music21

import util

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


'''
Feature: Number of notes in sample (a.k.a note density)
'''
def num_notes(piece):
    return len(util.get_notes(piece))


'''
Feature: Rhythmic variance
    Calculates the variance of the durations of the notes
'''
def rhythmic_variance(piece):
    notes = util.get_notes(piece)
    durations = list(map(lambda x: float(x.duration.quarterLength), notes))
    mean = numpy.mean(durations)
    sq_diff = reduce(lambda acc, x: acc + (x - mean) * (x - mean), durations)
    return sq_diff / len(notes)


'''
Feature: Rhythmic variety
    Calculates the percentage (multiplied by 10) of notes that have different durations
'''
def rhythmic_variety(piece):
    notes = util.get_notes(piece)
    durations = list(map(lambda x: float(x.duration.quarterLength), notes))
    num_durations = len(set(durations))
    return 10 * num_durations / len(notes)


'''
Feature: Leaps ratio
'''

'''
Feature: Range of melody
'''
def range_melody(piece):
    notes = util.get_notes(piece)
    note_values = list(map(lambda x: x.midi, notes))
    return max(note_values)-min(note_values)


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
