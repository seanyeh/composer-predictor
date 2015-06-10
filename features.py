#!/usr/bin/env python3

import inspect
import operator
import sys

from functools import reduce
from scipy import stats

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
    Calculates the ratio of leaps to steps. A leap is considered a distance greater than 2 (a major 2nd)
'''
def leaps_ratio(piece):
    notes = util.get_notes(piece)
    note_values = list(map(lambda x: x.midi, notes))
    leaps = 0
    steps = 0
    for i in range(len(note_values)-1):
        distance = abs(note_values[i+1]-note_values[i])
        if distance > 2:
            leaps += 1
        else:
            steps += 1
    return leaps/(leaps+steps)


'''
Feature: Repeated notes
    Finds the most repeated note and returns the number of times it appears in the sample
'''
def repeated_notes(piece):
    notes = util.get_notes(piece)
    note_values = list(map(lambda x: x.midi, notes))
    return stats.mode(note_values)[1][0]


'''
Feature: Low notes
    Finds how much of the melody is below a certain note. For now the middle note is set at 64 or an E that is above middle C
'''
def Low_notes(piece):
    notes = util.get_notes(piece)
    note_values = list(map(lambda x: x.midi, notes))
    high = 0
    low = 0
    for i in range(len(note_values)):
        if note_values[i] > 64:
            high += 1
        else:
            low +=1
    return low/(low+high)



'''
Feature: Range of melody
'''
def range_melody(piece):
    notes = util.get_notes(piece)
    note_values = list(map(lambda x: x.midi, notes))
    return max(note_values)-min(note_values)


'''
Feature: Chromaticism
'''
def chromaticism(piece):
    notes = util.get_notes(piece)
    note_values = list(map(lambda x: x.midi, notes))
    is_chromatic = 0
    for i in range(len(note_values)-2):
        if ((note_values[i]-note_values[i+1] == 1) and (note_values[i+1]-note_values[i+2] == 1)) or ((note_values[i+2]-note_values[i+1] == 1) and (note_values[i+1]-note_values[i] == 1)):
            is_chromatic = 1
    return is_chromatic


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
