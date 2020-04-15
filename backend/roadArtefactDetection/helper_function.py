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


def get_statistic_and_points(possible_points_grouped, bumps, realize_time):
    true_positives, false_positives, false_negatives = helpers.true_positives(
        possible_points_grouped, helpers.bumps_to_tuplepoints(bumps), 20)

    true_positives_count = len(true_positives)

    accuracy = float(0.0)
    if len(bumps) > 0:
        accuracy = float(true_positives_count / len(bumps) * 100)

    false_positives_count = len(false_positives)
    false_negatives_count = len(false_negatives)

    return {
        "acc": round(accuracy, 2),
        "tp": true_positives_count,
        "fp": false_positives_count,
        "fn": false_negatives_count,
        "time": round(realize_time*1000, 0)
    }, true_positives, false_positives, false_negatives


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
            statistic, tp, fp, fn = get_statistic_and_points(grouped_possible_artefacts, bumps, alg_result[1])
            prepared_tp = prepare_results(tp)
            prepared_fp = prepare_results(fp)
            prepared_fn = prepare_results(fn)
        else:
            error = True
            statistic = None
            prepared_tp = None
            prepared_fp = None
            prepared_fn = None

        algorithm_data = {
            "algorithmId": i,
            "algorithmName": ALGORITHM_NAMES[i],
            "error": error,
            "tp": prepared_tp,
            "fp": prepared_fp,
            "fn": prepared_fn,
            "stats": statistic
        }
        results.append(algorithm_data)
    return results
