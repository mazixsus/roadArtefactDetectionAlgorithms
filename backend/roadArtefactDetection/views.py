import os
import json
import time
import roadArtefactDetection.algorithms as algorithms
import roadArtefactDetection.helper_scripts.helpers as helpers

import pandas
from django.shortcuts import render
from django.http import HttpResponse

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
        "acc": accuracy,
        "tp": true_positives,
        "fp": false_positives,
        "fn": false_negatives,
        "time": realize_time
    }


def run_algorithms(data, bumps):
    results = []

    for i in range(0, 6):
        # prev_time = time.perf_counter()
        alg_result = get_alg_result(data)[i]
        # realize_time = time.perf_counter() - prev_time
        grouped_possible_artefacts = helpers.group_duplicates(alg_result[0], 20)
        statistic = get_statistic(grouped_possible_artefacts, bumps, alg_result[1])
        detected_bumps = prepare_results(grouped_possible_artefacts)
        algorithm_data = {
            "algorithmId": i,
            "algorithmName": ALGORITHM_NAMES[i],
            "detectedBumps": detected_bumps,
            "stats": statistic
        }
        results.append(algorithm_data)
    return results


def add_survey(request):
    file = request.FILES['survey']


def get_results(request):
    survey_id = request.GET['surveyId']
    filenames = os.listdir("./roadArtefactDetection/data/")
    file_path = "./roadArtefactDetection/data/"+filenames[int(survey_id)]
    bumps_file_path = "./roadArtefactDetection/bumps/"+filenames[int(survey_id)].replace(".csv", "(bumps).csv")
    data = pandas.read_csv(file_path, parse_dates=['Time'])
    bumps = pandas.read_csv(bumps_file_path)
    result = run_algorithms(data, bumps)
    return HttpResponse(result)


def get_survey_names(request):
    print(os.listdir("./"))
    filenames = os.listdir("./roadArtefactDetection/data/")

    result = []
    for index, filename in enumerate(filenames, start=0):
        file = {"surveyId": index, "fileName": filename}
        result.append(file)

    print(json.dumps(result))
    return HttpResponse(json.dumps(result))


def get_bumps(request):
    survey_id = request.GET['surveyId']
    filenames = os.listdir("./roadArtefactDetection/bumps/")
    bumps = pandas.read_csv("./roadArtefactDetection/bumps/"+filenames[int(survey_id)])
    bumps_tuplepoints = helpers.bumps_to_tuplepoints(bumps)
    return HttpResponse(prepare_results(bumps_tuplepoints))
