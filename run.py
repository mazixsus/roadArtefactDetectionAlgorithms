import sys
import pandas
import algorithms
import helper_scripts.helpers as helpers
import glob
import time
import os


def check_statistic(possible_points_grouped, bumps, threshold):
    true_positives = helpers.true_positives(
        possible_points_grouped, helpers.bumps_to_tuplepoints(bumps), 20)

    accuracy = float(0.0)
    if len(bumps) > 0:
        accuracy = float(len(true_positives) / len(bumps) * 100)

    print("TP: {0} Acc: ({3:.2f}%) FP: {1} FN: {2} Threshold: {4}".format(
        len(true_positives),
        len(possible_points_grouped) - len(true_positives),
        len(bumps) - len(true_positives),
        accuracy,
        threshold
    ))


def main():
    # print(os.listdir("./data/"))

    data_paths = glob.glob("./data/*.csv")
    bumps_paths = glob.glob("./bumps/*.csv")
    csv_results = list()
    for x in data_paths:
        csv_results.append(x.replace(".csv", "_result.csv").replace("data", "results"))

    for data_index in range(len(data_paths)):
        data = pandas.read_csv(data_paths[data_index], parse_dates=['Time'])
        bumps = pandas.read_csv(bumps_paths[data_index])

        # threshold for z-thresh: 1.2, z-diff: 3, stdev(Z): 0.25, g-zero: 0.8
        threshold = 1.2
        window_size = 5

        prevtime = time.perf_counter()
        result = algorithms.z_thresh(data, threshold)
        # result = algorithms.z_diff(data, threshold)
        # result = algorithms.stdev_alg(data, threshold, window_size)
        # result = algorithms.g_zero(data, threshold)
        print("Alg time: {0}".format(time.perf_counter()-prevtime))

        prevtime = time.perf_counter()
        grouped_possible_artefacts = helpers.group_duplicates(result, 20)
        print("Grup time: {0}".format(time.perf_counter() - prevtime))

        prevtime = time.perf_counter()
        check_statistic(grouped_possible_artefacts, bumps, threshold)
        print("Stat time: {0}".format(time.perf_counter() - prevtime))
        print("---------------------------------------------------------")

        grouped_possible_artefacts_df = pandas.DataFrame(grouped_possible_artefacts, columns=["Latitude", "Longitude"])
        grouped_possible_artefacts_df.to_csv(csv_results[data_index], index=False)


if __name__ == '__main__':
    main()
