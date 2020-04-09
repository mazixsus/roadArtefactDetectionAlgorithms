"""
F-THRESH calculating threshold for current reading
"""
import pandas
import numpy
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from roadArtefactDetection.helper_scripts import rrui


def quality_mf(variant):
    quality = ctrl.Antecedent(numpy.arange(0, 8, 1), 'quality')

    if variant == 1:
        # automated three classes of road quality
        quality.automf(3, names=['good', 'mediocre', 'poor'])
    else:
        quality['good'] = fuzz.gaussmf(quality.universe, 0, 2)
        quality['mediocre'] = fuzz.gaussmf(quality.universe, 3, 1)
        quality['poor'] = fuzz.gaussmf(quality.universe, 6, 2)

    return quality


def threshold_mf(variant):
    # threshold = ctrl.Consequent(numpy.arange(3, 6, 1), 'threshold')
    threshold = ctrl.Consequent(numpy.arange(3, 6, 0.2), 'threshold')

    if variant == 1:
        threshold['low'] = fuzz.trimf(threshold.universe, [0, 3, 4])
        threshold['medium'] = fuzz.trimf(threshold.universe, [3, 4.3, 5])
        threshold['high'] = fuzz.trimf(threshold.universe, [4, 5, 5]) 
    elif variant == 2:   
        threshold['low'] = fuzz.trimf(threshold.universe, [0, 3, 4.3])    
        threshold['medium'] = fuzz.gaussmf(threshold.universe, 4.3, 0.2)    
        threshold['high'] = fuzz.trimf(threshold.universe, [4.0, 4.5, 5])
    elif variant == 3:
        threshold['low'] = fuzz.gaussmf(threshold.universe, 3.5, 0.2)
        threshold['medium'] = fuzz.gaussmf(threshold.universe, 4.3, 0.2)
        threshold['high'] = fuzz.gaussmf(threshold.universe, 4.9, 0.2)
    elif variant == 4:
        threshold['low'] = fuzz.gaussmf(threshold.universe, 3.5, 0.3)
        threshold['medium'] = fuzz.gaussmf(threshold.universe, 4.3, 0.3)
        threshold['high'] = fuzz.gaussmf(threshold.universe, 5.0, 0.3)

    return threshold


def possible(data, qvariant, tvariant):
    """
    Find possible indexes of road artefacts using the
    F-THRESH algorithm
    """
    result = []

    # set inputs: road quality and reading value
    quality = quality_mf(qvariant)

    reading = ctrl.Antecedent(numpy.arange(0, 2, 1), 'reading')
    reading.automf(2, names=['low', 'high'])

    # output value: threshold
    threshold = threshold_mf(tvariant)
    
    stdZ2 = data['Z2'].agg('std')
    avgZ2 = data['Z2'].agg('average')

    # calculate RRUI class for this data

    rrui_class = rrui.classify_number(rrui.calculate(data))

    # create set of rules
    rules = [
        ctrl.Rule(quality['poor'] | reading['high'], threshold['high']),
        ctrl.Rule(quality['good'] | reading['low'], threshold['low']),
        # ctrl.Rule(quality['mediocre'] | reading['low'], threshold['medium'])
        # ctrl.Rule(quality['mediocre'] | reading['high'], threshold['high'])
    ]

    system = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
    system.input['quality'] = rrui_class

    # for i in range(len(data) - 1):
    #     # calculate difference between current reading and average in
    #     # this data window
    #     difference = abs(data['Z2'][i:i + 1].iloc[0] - avgZ2)
    #
    #     # recalculate threshold for current data window and reading
    #     system.input['reading'] = difference
    #     system.compute()
    #
    #     # print(stdZ2 * system.output['threshold'])
    #     # print(difference)
    #
    #     # check if it is possible problem
    #     if difference > (stdZ2 * system.output['threshold']):
    #         result.append(i)

    for index, survey in data.iterrows():
        # calculate difference between current reading and average in
        # this data window
        difference = abs(survey[5] - avgZ2)

        # recalculate threshold for current data window and reading
        system.input['reading'] = difference
        system.compute()

        # print(stdZ2 * system.output['threshold'])
        # print(difference)

        # check if it is possible problem
        if difference > (stdZ2 * system.output['threshold']):
            result.append(survey[6:8])

    return result
