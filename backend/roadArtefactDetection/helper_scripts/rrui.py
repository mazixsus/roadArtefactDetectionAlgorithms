import pandas, numpy
from roadArtefactDetection.helper_scripts import helpers
from math import radians, cos, sin, asin, sqrt
from functools import reduce


def rruiA_calculate():
    """
    Returns "default" A value for RRUI, by recalculating over a 1000 meters 
    segment of A class road
    """
    rrui_finger = pandas.read_csv(r"E:\Marcin\OneDrive\Uczelnia\Doktorat\Przejazdy-CRADIA\2015-05-21 13-23-50.csv",
                                  parse_dates=['Time'])
    start, stop = helpers.distance_window(rrui_finger, 3176, 1000)
    return rrui_finger[start:stop]['Z2'].agg('std')


A = 0.0497428974060465  # default RRUI_A value, as calculated by the function


def calculate(data, a_fp=A):
    sigmaz = data['Z2'].agg('std')
    return (sigmaz - a_fp) * 100


def segments(data, window, a_fp):
    """
    Calculates RRUI values for a specified data by a window of a specified
    distance, where a_fp is a fingerprint value for the "best" road
    """
    segments = []

    start = 0

    while start < len(data) - 1:
        start, stop = helpers.distance_window(data, start, window)
        sigmaz = data[start:stop]['Z2'].agg('std')
        rruiv = (sigmaz - a_fp) * 100
        rclass = classify(rruiv)

        segments.append(
            (
                data[['Latitude', 'Longitude']][start:start + 1].values[0],
                data[['Latitude', 'Longitude']][stop:stop + 1].values[0],
                rruiv,
                rclass
            ))

        start = stop

    return segments


def segment_tuple_to_dict(segment):
    return {'Start_Latitude': segment[0][0],
            'Start_Longitude': segment[0][1],
            'End_Latitude': segment[1][0],
            'End_Longitude': segment[1][1],
            'RRUI': segment[2],
            'Class': segment[3]
            }


def classify(value):
    thresholds = [6, 12, 17, 24, 30, 36]
    classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for i in thresholds:
        if value <= i:
            return classes[thresholds.index(i)]

    return 'H'


def classify_number(value):
    classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    return classes.index(classify(value))
