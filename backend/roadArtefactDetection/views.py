import os
import json
import time
import roadArtefactDetection.algorithms as algorithms
import roadArtefactDetection.helper_scripts.helpers as helpers

import pandas
from django.shortcuts import render
from django.http import HttpResponse

ALGORITHM_NAMES = ["Z-THRESH", "Z-DIFF", "STDEV", "G-ZERO", "MOD-Z-THRESH", "F-THRESH"]


def new_view(request):
    return HttpResponse("")


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


def get_alg_result(data):
    return {
        1: algorithms.z_thresh(data, 1.2),
        2: algorithms.z_diff(data, 3),
        3: algorithms.stdev_alg(data, 0.25, 50),
        4: algorithms.g_zero(data, 0.8),
        5: algorithms.mod_z_thresh(data, 4.3),
        6: algorithms.f_thresh(data, 50, 1, 1)
    }


def get_statistic(possible_points_grouped, bumps, realize_time):
    true_positives = helpers.true_positives(
        possible_points_grouped, helpers.bumps_to_tuplepoints(bumps), 20)

    accuracy = float(0.0)
    if len(bumps) > 0:
        accuracy = float(len(true_positives) / len(bumps) * 100)

    false_positives = len(possible_points_grouped) - len(true_positives)
    false_negatives = len(bumps) - len(true_positives)
    return {
        "acc": accuracy,
        "tp": true_positives,
        "fp": false_positives,
        "fn": false_negatives,
        "time": realize_time
    }


def run_algorithms(filename):
    data = pandas.read_csv("./roadArtefactDetection/data/"+filename)
    bumps = pandas.read_csv("./roadArtefactDetection/bumps/"+filename.replace(".csv", "_result.csv"))

    results = []

    for i in range(1, 7):
        prev_time = time.perf_counter()
        alg_result = get_alg_result(data)[i]
        realize_time = time.perf_counter() - prev_time
        grouped_possible_artefacts = helpers.group_duplicates(alg_result, 20)
        statistic = get_statistic(grouped_possible_artefacts, bumps, realize_time)
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
    survey_id = request.GET['surveyID']
    filenames = os.listdir("./roadArtefactDetection/data/")
    data = run_algorithms(filenames[survey_id])
    return HttpResponse(data)


def get_survey_names(request):
    print(os.listdir("./"))
    filenames = os.listdir("./roadArtefactDetection/data/")

    data = []
    for index, filename in enumerate(filenames, start=0):
        file = {"surveyId": index, "fileName": filename}
        data.append(file)

    print(json.dumps(data))
    return HttpResponse(json.dumps(data))


def get_bumps(request):
    survey_id = request.GET['surveyId']
    filenames = os.listdir("./roadArtefactDetection/bumps/")
    bumps = pandas.read_csv("./roadArtefactDetection/bumps/"+filenames[int(survey_id)])
    bumps_tuplepoints = helpers.bumps_to_tuplepoints(bumps)
    return HttpResponse(prepare_results(bumps_tuplepoints))
