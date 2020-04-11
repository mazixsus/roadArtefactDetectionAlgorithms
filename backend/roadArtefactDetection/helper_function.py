import os
import signal
import time
from threading import Thread

from roadArtefactDetection import algorithms
from roadArtefactDetection.helper_scripts import helpers

ALGORITHM_NAMES = ["Z-THRESH", "Z-DIFF", "STDEV", "G-ZERO", "MOD-Z-THRESH", "F-THRESH"]


def prepare_results(artefacts_positions):
    surveys = []
    for artefact in artefacts_positions:
        surveys.append(
            {
                "lat": artefact[0],
                "lng": artefact[1]
            }
        )
    return surveys


def count_time(function, *args):
    prev_time = time.perf_counter()
    result = function(*args)
    realize_time = time.perf_counter() - prev_time
    return result, realize_time


def get_alg_result(data):
    return {
        0: count_time(algorithms.z_thresh, data, 1.2),
        1: count_time(algorithms.z_diff, data, 3),
        2: count_time(algorithms.stdev_alg, data, 0.25, 50),
        3: count_time(algorithms.g_zero, data, 0.8),
        4: count_time(algorithms.mod_z_thresh, data, 4.3),
        5: count_time(algorithms.f_thresh, data, 50, 1, 1)
    }


def get_statistic(possible_points_grouped, bumps, realize_time):
    true_positives_points = helpers.true_positives(
        possible_points_grouped, helpers.bumps_to_tuplepoints(bumps), 20)

    true_positives = len(true_positives_points)

    accuracy = float(0.0)
    if len(bumps) > 0:
        accuracy = float(len(true_positives_points) / len(bumps) * 100)

    false_positives = len(possible_points_grouped) - len(true_positives_points)
    false_negatives = len(bumps) - len(true_positives_points)
    return {
        "acc": round(accuracy, 2),
        "tp": true_positives,
        "fp": false_positives,
        "fn": false_negatives,
        "time": round(realize_time*1000, 0)
    }


def handle_uploaded_file(path, file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def save_files(data_file, bumps_file, data_path, bumps_path):
    filenames = os.listdir(data_path)
    counter = 0
    data_file_name = data_file.name
    if data_file_name in filenames:
        data_file_name = data_file_name.replace(".csv", "(" + str(counter) + ").csv")
        while data_file_name in filenames:
            counter += 1
            data_file_name = data_file_name.replace("(" + str(counter - 1) + ").csv", "(" + str(counter) + ").csv")

    data_file_path = data_path + data_file_name
    bumps_file_path = bumps_path + data_file_name.replace('.csv', '(bumps).csv')
    handle_uploaded_file(data_file_path, data_file)
    handle_uploaded_file(bumps_file_path, bumps_file)

    filenames = os.listdir(data_path)
    print(filenames.index(data_file_name))

    return filenames.index(data_file_name)


def run_algorithms(data, bumps, timeout):
    results = []

    for i in range(0, 6):
        alg_result = get_alg_result(data)[i]
        grouped_possible_artefacts = helpers.group_duplicates(alg_result[0], 20, timeout)
        if grouped_possible_artefacts is not None:
            error = False
            statistic = get_statistic(grouped_possible_artefacts, bumps, alg_result[1])
            detected_bumps = prepare_results(grouped_possible_artefacts)
        else:
            error = True
            statistic = None
            detected_bumps = None

        algorithm_data = {
            "algorithmId": i,
            "algorithmName": ALGORITHM_NAMES[i],
            "error": error,
            "detectedBumps": detected_bumps,
            "stats": statistic
        }
        results.append(algorithm_data)
    return results
