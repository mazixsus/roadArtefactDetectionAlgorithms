import math
import statistics

import helper_scripts.helpers as helpers
from helper_scripts import fthresh


def z_thresh(data, threshold):
    """
    Check if Z2 pass threshold and return potential artefacts latitude and longitude
    """
    result = list()
    for index, survey in data.iterrows():

        if abs(survey[5]) > threshold:
            result.append(survey[6:8])
    # print("{0}".format(result))
    return result


def z_diff(data, threshold):
    """
    Check if (Z2_n - Z_n-1)/(Time_n - Time_n-1) pass threshold and return potential artefacts latitude and longitude
    """
    result = list()
    prev_survey = None
    if_first = True
    for index, survey in data.iterrows():
        if if_first:
            prev_survey = survey
            if_first = False
            continue

        diff = (survey[5] - prev_survey[5]) / (survey[8] - prev_survey[8]).total_seconds()
        # print(abs(diff))
        if abs(diff) > threshold:
            result.append(survey[6:8])
        # print("{0}".format(result))
        prev_survey = survey
    return result


def stdev_alg(data, threshold, window_size):
    result = list()
    for index, survey in data[window_size:].iterrows():
        zaxis_data_window = list(data.iloc[list(range(index - window_size, index)), 5])
        stdev_val = statistics.stdev(zaxis_data_window)
        # print(stdev_val)
        if stdev_val > threshold:
            result.append(survey[6:8])
    return result


# def stdev_alg(data, threshold, window_size):
#     result = list()
#     for surveys_window in helpers.tumbling_window(data, window_size):
#         stdev_val = statistics.stdev(surveys_window['Z2'])
#         if stdev_val > threshold:
#             # print((surveys_window['Latitude'], surveys_window['Longitude']))
#             result.append((surveys_window['Latitude'], surveys_window['Longitude']))
#     print(result)
#     return result

def g_zero(data, threshold):
    """
    Check if summary acceleration value sqrt(ax^2 + ay^2 + az^2) pass threshold and return potential artefacts latitude
    and longitude
    """
    result = list()
    for index, survey in data.iterrows():
        a = math.sqrt(survey[3] ** 2 + survey[4] ** 2 + survey[5] ** 2)
        # print(a)
        if a < threshold:
            result.append(survey[6:8])
    # print("{0}".format(result))
    return result


def f_thresh(data, window_size, quality_variant, threshold_variant):
    result = list()
    for i in helpers.tumbling_window(data, window_size):
        for j in fthresh.possible(i, quality_variant, threshold_variant):
            p = i[j:j + 1][['Latitude', 'Longitude']].values[0]
            result.append((p[0], p[1]))
    return result


def mod_z_thresh(data, threshold):
    """
    Find possible indexes of road artefacts using the
    MOD Z-THRESH algorithm
    """
    result = list()
    stdZ2 = data['Z2'].agg('std')
    avgZ2 = data['Z2'].agg('average')
    for index, survey in data.iterrows():
        if abs(survey[5] - avgZ2) > (stdZ2 * threshold):
            result.append(survey[6:8])
    return result
