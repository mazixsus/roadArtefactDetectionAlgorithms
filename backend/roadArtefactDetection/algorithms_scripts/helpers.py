"""
CRADIA helper functions
"""
import time
from math import radians, cos, sin, asin, sqrt
from functools import reduce
import numpy


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    meters = 6371000 * c
    return meters


def haversine_point(point1, point2):
    """
    Calculate the distance between two points on the earth
    where points are represented as pairs Lat,Lon
    """
    return haversine(point1[1], point1[0], point2[1], point2[0])


def total_distance(data):
    """
    Calculates the distance on all dataframe in meters
    """
    result = 0.0

    for i in range(len(data) - 1):
        result += haversine_point(data[i:i + 1].as_matrix(['Latitude', 'Longitude'])[0],
                                  data[i + 1:i + 2].as_matrix(['Latitude', 'Longitude'])[0])

    return result


def geopoint(data, index):
    """
    Gets the physical location for the point on the specified index
    in the data table
    """
    return data[['Latitude', 'Longitude']][index:index + 1]


def geopoint_raw(point):
    """
    Changes complex object into an array of latitude and longitude
    """
    return point.values[0]


def bump_tuplepoint(bumps, index):
    """
    Returns bump of a specified index as a pair of latitude and longitude
    """
    bump = bumps[index:index + 1].values[0]
    return bump[0], bump[1]


def true_positives_v1(possible_tuplepoints, bumps_tuplepoints, distance):
    """
    Returns true positives: points, which are in the near distance
    to the points marked by the user as the real artefacts
    """

    results = set()
    if len(bumps_tuplepoints) == 0 or len(possible_tuplepoints) == 0:
        return results

    for i in range(len(bumps_tuplepoints)):
        for j in range(len(possible_tuplepoints)):
            if haversine_point(bumps_tuplepoints[i], possible_tuplepoints[j]) < distance:
                results.add(possible_tuplepoints[j].iloc(0))
                break

    return results

def true_positives(possible_tuplepoints, bumps_tuplepoints, distance):
    """
    Returns true positives: points, which are in the near distance
    to the points marked by the user as the real artefacts
    """

    tp = []
    fp = []
    fn = []
    if len(bumps_tuplepoints) == 0:
        return tp, fp, fn

    if len(possible_tuplepoints) == 0:
        fn = bumps_tuplepoints
        return tp, fp, fn

    is_detected = False
    for i in range(len(bumps_tuplepoints)):
        for j in range(len(possible_tuplepoints)):
            if haversine_point(bumps_tuplepoints[i], possible_tuplepoints[j]) < distance:
                tp.append(possible_tuplepoints[j])
                is_detected = True
                break
        if not is_detected:
            fn.append(bumps_tuplepoints[i])
        is_detected = False

    # print("----------------------possible_tuplepoints-----------------------")
    # print(possible_tuplepoints)
    # print("--------------------------tp---------------------------------")
    # print(tp)

    is_tp = False
    for possible_survey in possible_tuplepoints:
        for tp_survey in tp:
            if possible_survey[0] == tp_survey[0] and possible_survey[1] == tp_survey[1]:
                is_tp = True
                break
        if not is_tp:
            fp.append(possible_survey)
        is_tp = False

    # print("---------------------------fp-------------------------------")
    # print(fp)
    # print("--------------------------fn-------------------------------")
    # print(fn)

    return tp, fp, fn


def bumps_to_tuplepoints(bumps):
    bumps_tuplepoints = []
    for i in range(len(bumps)):
        bumps_tuplepoints.append(bump_tuplepoint(bumps, i))

    return bumps_tuplepoints


def indices_to_tuplepoints(indices, data):
    points = []
    for i in range(len(indices)):
        poi = geopoint(data, indices[i]).values[0]
        points.append((poi[0], poi[1]))
    return points


def group_duplicates(tuplepoints, distance, timeout):
    """
    Groups duplicates - points which are in the radious of a defined distance
    a grouped into one    
    """
    result = []
    start_time = time.perf_counter()

    for i in range(len(tuplepoints)):
        found = False
        for j in range(len(result)):
            if haversine_point(tuplepoints[i], result[j]) < distance:
                found = True

        if not found:
            result.append(tuplepoints[i])

        if time.perf_counter() - start_time > timeout:
            return None

    return result


def distance_window(data, start, size):
    """
    Calculates the indices of start and ending position from a datastream in search for a window
    of a specified size (in meters)
    """

    result = 0.0

    for i in range(start, len(data) - 1):
        result += haversine_point(data[i:i + 1].as_matrix(['Latitude', 'Longitude'])[0],
                                  data[i + 1:i + 2].as_matrix(['Latitude', 'Longitude'])[0])
        if result >= size:
            return start, i

    return start, len(data) - 1


def tumbling_window(data, window):
    for i in range(int(len(data) / window)):
        yield data[i * window:(i * window + window)]


def sliding_window(data, window, step):
    for i in range(int((len(data) - window - step) / step) + 2):
        yield data[i * step:i * step + window]
