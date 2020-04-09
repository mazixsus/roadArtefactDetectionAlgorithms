import os
import json
import roadArtefactDetection.helper_scripts.helpers as helpers
import pandas

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from roadArtefactDetection.helper_function import run_algorithms, prepare_results, save_files

DATA_PATH = './roadArtefactDetection/data/'
BUMPS_PATH = './roadArtefactDetection/bumps/'
DATA_COL_LABEL = ['X', 'Y', 'Z', 'N', 'E', 'Z2', 'Latitude', 'Longitude', 'Time', 'Speed', 'Course', 'Accuracy']
BUMPS_COL_LABEL = ['Latitude', 'Longitude']
TIMEOUT = 5


@csrf_exempt
def add_survey(request):

    if request.method != 'POST' or 'survey' not in request.FILES or 'bumps' not in request.FILES:
        return HttpResponse(status=400)

    data_file = request.FILES['survey']
    bumps_file = request.FILES['bumps']
    data_file_name = data_file.name

    print(data_file_name.endswith('.csv'))
    if not data_file_name.endswith('.csv'):
        return HttpResponse('File is not csv.', status=400)

    csv_data_file = pandas.read_csv(data_file)
    csv_bumps_file = pandas.read_csv(bumps_file)

    if not (csv_bumps_file.columns == BUMPS_COL_LABEL).all():
        return HttpResponse('Bumps file not valid.')

    if not (csv_data_file.columns == DATA_COL_LABEL).all():
        return HttpResponse('Data file not valid.')

    file_path, bumps_file_path = save_files(data_file, bumps_file, DATA_PATH, BUMPS_PATH)

    data = pandas.read_csv(file_path, parse_dates=['Time'])
    bumps = pandas.read_csv(bumps_file_path)
    result = run_algorithms(data, bumps, TIMEOUT)

    return HttpResponse(result)


def get_results(request):

    if request.method != 'GET' or 'surveyId' not in request.GET:
        return HttpResponse(status=400)

    survey_id_str = request.GET['surveyId']

    try:
        survey_id = int(survey_id_str)
    except ValueError:
        return HttpResponse(status=400)

    filenames = os.listdir(DATA_PATH)
    file_path = DATA_PATH+filenames[survey_id]
    bumps_file_path = BUMPS_PATH+filenames[survey_id].replace(".csv", "(bumps).csv")
    data = pandas.read_csv(file_path, parse_dates=['Time'])
    bumps = pandas.read_csv(bumps_file_path)
    result = run_algorithms(data, bumps, TIMEOUT)
    return HttpResponse(result)


def get_survey_names(request):

    if request.method != 'GET':
        return HttpResponse(status=400)

    print(os.listdir("./"))
    filenames = os.listdir(DATA_PATH)

    result = []
    for index, filename in enumerate(filenames, start=0):
        file = {"surveyId": index, "fileName": filename}
        result.append(file)

    print(json.dumps(result))
    return HttpResponse(json.dumps(result))


def get_bumps(request):

    if request.method != 'GET' or 'surveyId' not in request.GET:
        return HttpResponse(status=400)

    survey_id_str = request.GET['surveyId']

    try:
        survey_id = int(survey_id_str)
    except ValueError:
        return HttpResponse(status=400)

    filenames = os.listdir(BUMPS_PATH)
    bumps = pandas.read_csv(BUMPS_PATH+filenames[survey_id])
    bumps_tuplepoints = helpers.bumps_to_tuplepoints(bumps)
    return HttpResponse(prepare_results(bumps_tuplepoints))
