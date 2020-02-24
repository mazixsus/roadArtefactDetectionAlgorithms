import math
import statistics

import helper_scripts.helpers as helpers


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
    result = list()
    prev_survey = None
    if_first = True
    for index, survey in data.iterrows():
        if if_first:
            prev_survey = survey
            if_first = False
            continue

        diff = (survey[5]-prev_survey[5])/(survey[8]-prev_survey[8]).total_seconds()
        # print(abs(diff))
        if abs(diff) > threshold:
            result.append(survey[6:8])
    # print("{0}".format(result))
        prev_survey = survey
    return result


def stdev_alg(data, threshold, window_size):
    result = list()
    for index, survey in data[window_size:].iterrows():
        zaxis_data_window = list(data.iloc[list(range(index-window_size, index)), 5])
        stdev_val = statistics.stdev(zaxis_data_window)
        if stdev_val > threshold:
            result.append(survey[6:8])
    return result


def g_zero(data, threshold):
    result = list()
    for index, survey in data.iterrows():
        a = math.sqrt(survey[3] ^ 2 + survey[4] ^ 2 + survey[5] ^ 2)
        if a < threshold:
            result.append(survey[6:8])
    # print("{0}".format(result))
    return result

