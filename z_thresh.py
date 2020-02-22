import helper_scripts.helpers as helpers


def z_thresh(data, threshold):
    possible_artefacts = find_possible_artefacts(data, threshold)
    grouped_possible_artefacts = helpers.group_duplicates(possible_artefacts, 20)

    return grouped_possible_artefacts


def find_possible_artefacts(data, threshold):
    """
    Check if Z2 pass threshold and return potential artefacts latitude and longitude
    """
    result = list()
    for index, survey in data.iterrows():

        if abs(survey[5]) > threshold:
            result.append(survey[6:8])
    # print("{0}".format(result))
    return result
