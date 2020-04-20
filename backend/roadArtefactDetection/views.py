import os
import json
import roadArtefactDetection.helper_scripts.helpers as helpers
import pandas
import math
import datetime
from decimal import *
from dateutil.parser import parse

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from roadArtefactDetection.helper_function import run_algorithms, prepare_results, save_files, save_files_v2

DATA_PATH = './roadArtefactDetection/data/'
BUMPS_PATH = './roadArtefactDetection/bumps/'
DATA_COL_LABEL = ['X', 'Y', 'Z', 'N', 'E', 'Z2', 'Latitude', 'Longitude', 'Time', 'Speed', 'Course', 'Accuracy']
BUMPS_COL_LABEL = ['Latitude', 'Longitude']
TIMEOUT = 5


@csrf_exempt
def add_survey(request):
    if request.method != 'POST' or 'survey' not in request.FILES or 'bumps' not in request.FILES:
        return HttpResponse('Błędne zapytanie.', status=400)

    data_file = request.FILES['survey']
    bumps_file = request.FILES['bumps']
    data_file_name = data_file.name

    if not data_file_name.endswith('.csv'):
        return HttpResponse('Przesłany plik nie jest w formacie csv.', status=400)

    try:
        csv_data_file = pandas.read_csv(data_file, parse_dates=['Time'])
    except ValueError:
        return HttpResponse('Błędna struktura pliku z pomiarami.', status=400)
    csv_bumps_file = pandas.read_csv(bumps_file)

    if len(csv_bumps_file.columns) != len(BUMPS_COL_LABEL) or not (csv_bumps_file.columns == BUMPS_COL_LABEL).all() \
            or csv_bumps_file.shape[0] < 1:
        return HttpResponse('Błędna struktura pliku z progami.', status=400)

    if len(csv_data_file.columns) != len(DATA_COL_LABEL) or not (csv_data_file.columns == DATA_COL_LABEL).all()\
            or csv_data_file.shape[0] < 10:
        return HttpResponse('Błędna struktura pliku z pomiarami.', status=400)

    csv_data_file = prepare_data_csv(csv_data_file)
    csv_bumps_file = prepare_bumps_csv(csv_bumps_file)

    if csv_bumps_file.shape[0] < 1:
        return HttpResponse('Plik z progami nie posiada danych o żadnym progu.', status=400)

    if csv_data_file.shape[0] < 10:
        return HttpResponse('Plik z pomiarami posiada mniej niż 10 poprawnych pomiarów.', status=400)

    survey_id = save_files(csv_data_file, csv_bumps_file, data_file_name, DATA_PATH, BUMPS_PATH)

    result = {
        "surveyId": survey_id,
    }

    return HttpResponse(json.dumps(result))


def prepare_bumps_csv(csv_bumps_file):
    indexes = []
    for index, row in csv_bumps_file.iterrows():
        for value in row[0:2]:
            if value == 0 or check_numeric(value):
                indexes.append(index)
                break
    return csv_bumps_file.drop(indexes)


def prepare_data_csv(csv_data_file):
    indexes = []
    for index, row in csv_data_file.iterrows():
        if not check_date(row[8]):
            indexes.append(index)
            continue
        for value in row[0:8]:
            if value == 0 or check_numeric(value):
                indexes.append(index)
                break
    print("Deleted indexes:" + str(indexes))
    return csv_data_file.drop(indexes)


def check_date(date):
    try:
        parse(date)
    except ValueError:
        return False
    except TypeError:
        try:
            isinstance(date, pandas.Timestamp)
            return not pandas.isna(date)
        except TypeError:
            return False
    return True


def check_numeric(value):
    try:
        float_value = float(value)
    except ValueError:
        return True
    return math.isnan(float_value)


def get_results(request):
    if request.method != 'GET' or 'surveyId' not in request.GET:
        return HttpResponse('Błędne zapytanie.', status=400)

    survey_id_str = request.GET['surveyId']

    try:
        survey_id = int(survey_id_str)
    except ValueError:
        return HttpResponse('Błędne zapytanie.', status=400)

    filenames = os.listdir(DATA_PATH)
    file_path = DATA_PATH + filenames[survey_id]
    bumps_file_path = BUMPS_PATH + filenames[survey_id].replace(".csv", "(bumps).csv")
    data = pandas.read_csv(file_path, parse_dates=['Time'])
    bumps = pandas.read_csv(bumps_file_path)
    result = run_algorithms(data, bumps, TIMEOUT)
    return HttpResponse(json.dumps(result))


def get_survey_names(request):
    if request.method != 'GET':
        return HttpResponse('Błędne zapytanie.', status=400)

    filenames = os.listdir(DATA_PATH)

    result = []
    for index, filename in enumerate(filenames, start=0):
        file = {"surveyId": index, "fileName": filename}
        result.append(file)

    return HttpResponse(json.dumps(result))


def get_bumps(request):
    if request.method != 'GET' or 'surveyId' not in request.GET:
        return HttpResponse('Błędne zapytanie.', status=400)

    survey_id_str = request.GET['surveyId']

    try:
        survey_id = int(survey_id_str)
    except ValueError:
        return HttpResponse('Błędne zapytanie.', status=400)

    filenames = os.listdir(BUMPS_PATH)
    bumps = pandas.read_csv(BUMPS_PATH + filenames[survey_id])
    bumps_tuplepoints = helpers.bumps_to_tuplepoints(bumps)
    return HttpResponse(json.dumps(prepare_results(bumps_tuplepoints)))
