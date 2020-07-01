import os
import pandas
import math
from dateutil.parser import parse


def handle_uploaded_file(path, file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def save_files(data_file, bumps_file, data_file_name, data_path, bumps_path):
    filenames = os.listdir(data_path)
    counter = 0
    if data_file_name in filenames:
        data_file_name = data_file_name.replace(".csv", "(" + str(counter) + ").csv")
        while data_file_name in filenames:
            counter += 1
            data_file_name = data_file_name.replace("(" + str(counter - 1) + ").csv", "(" + str(counter) + ").csv")

    data_file_path = data_path + data_file_name
    bumps_file_path = bumps_path + data_file_name.replace('.csv', '(bumps).csv')
    data_file.to_csv(data_file_path, index=False)
    bumps_file.to_csv(bumps_file_path, index=False)

    filenames = os.listdir(data_path)
    print(filenames.index(data_file_name))

    return filenames.index(data_file_name)


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
