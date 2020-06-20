import math
import statistics

import roadArtefactDetection.algorithms_scripts.helpers as helpers
from roadArtefactDetection.algorithms_scripts import fthresh


def z_thresh(data, threshold):
    """
    Check if Z2 pass threshold and return potential artefacts latitude and longitude
    """
    result = list()
    for index, survey in data.iterrows():
        if abs(survey[5]) > threshold:
            result.append(survey[6:8])
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
        if abs(diff) > threshold:
            result.append(survey[6:8])
        prev_survey = survey
    return result


def stdev_alg(data, threshold, window_size):
    result = list()
    for index, survey in data[window_size:].iterrows():
        zaxis_data_window = list(data.iloc[list(range(index - window_size, index)), 5])
        stdev_val = statistics.stdev(zaxis_data_window)
        if stdev_val > threshold:
            result.append(survey[6:8])
    return result


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
    return result


def f_thresh(data, window_size, quality_variant, threshold_variant):
    result = list()
    for i in helpers.tumbling_window(data, window_size):
        for j in fthresh.possible(i, quality_variant, threshold_variant):
            result.append(j)
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


# def my_alg(data, window_size):
#     result = list()
#     global_avg = 0
#     start_diff = 0.2
#
#     global_diff = start_diff
#     for i in helpers.tumbling_window(data, window_size):
#         sorted_i = i.sort_values(by=['Z2'])
#         index = 0
#         artefact_sector = 0
#         break_diff = 0
#         avg_end = 0
#
#         for j in helpers.tumbling_window(sorted_i, 5):
#             if index == 0:
#                 prev_avg = j.Z2.agg('average')
#                 avg_end = prev_avg
#                 first_segment = j
#             else:
#                 curr_avg = j.Z2.agg('average')
#                 diff = abs(prev_avg - curr_avg)
#
#                 if (diff > global_diff) and (1 <= index <= 5):
#                     break_diff = diff
#                     artefact_sector = 1
#                     avg_end = curr_avg
#                 elif diff > start_diff and artefact_sector != 1:
#                     break_diff = diff
#                 prev_avg = curr_avg
#
#             index += 1
#
#         global_avg = (global_avg + avg_end)/2 if avg_end != 0 else global_avg
#         global_diff = (global_diff + break_diff)/2 if break_diff != 0 else global_diff
#
#         if artefact_sector == 1:
#             for index, survey in i.iterrows():
#                 if abs(survey[5]) > abs(global_avg)+global_diff:
#                     result.append(survey[6:8])
#         else:
#             for index, survey in first_segment.iterrows():
#                 if abs(survey[5]) > abs(global_avg)+global_diff:
#                     result.append(survey[6:8])
#
#     return result
