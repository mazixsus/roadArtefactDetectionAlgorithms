import math
import statistics
import numpy
from scipy.signal import argrelextrema

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
            result.append(j)
            # print(j)
            # p = i[j:j + 1][['Latitude', 'Longitude']].values[0]
            # result.append((p[0], p[1]))
    return result


def mod_z_thresh(data, threshold):
    """
    Find possible indexes of road artefacts using the
    MOD Z-THRESH algorithm
    """
    result = list()
    std_z2 = data['Z2'].agg('std')
    avg_z2 = data['Z2'].agg('average')
    for index, survey in data.iterrows():
        if abs(survey[5] - avg_z2) > (std_z2 * threshold):
            result.append(survey[6:8])
    return result


def my_alg(data, window_size):
    result = list()
    global_avg = 0
    global_diff = 0.12
    for i in helpers.tumbling_window(data, window_size):
        # print(argrelextrema(i['Z2'], numpy.greater))
        sorted_i = i.sort_values(by=['Z2'])
        # print(sorted_i)

        index = 0
        artefact_sector = 0
        avg = 0
        break_diff = 0
        avg_end = 0

        for j in helpers.tumbling_window(sorted_i, 5):
            if index == 0:
                prev_avg = j.Z2.agg('average')
                first_avg = prev_avg
                # print(prev_avg)
            else:
                curr_avg = j.Z2.agg('average')
                diff = abs(prev_avg - curr_avg)

                if (diff > 0.12) and (1 <= index <= 3):
                    break_diff = diff
                    artefact_sector = 1
                    avg = 0
                    avg_end = curr_avg
                elif index < 7:
                    avg = (avg + prev_avg)/2

                prev_avg = curr_avg
                # print(diff)
                # print("--------------------------------")

            index += 1
        # avg_end = avg if avg_end == 0 else avg_end
        avg_end = first_avg if avg_end == 0 else avg_end

        global_avg = (global_avg + avg_end)/2 if avg_end != 0 else global_avg
        global_diff = (global_diff + break_diff)/2 if break_diff != 0 else global_diff
        # global_diff = break_diff if break_diff != 0 else global_diff

        # print(artefact_sector)

        if artefact_sector == 1:
            for index, survey in i.iterrows():
                if abs(survey[5]) > abs(global_avg)+global_diff:
                    result.append(survey[6:8])

    return result
