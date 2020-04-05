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

    data_paths = [
        "./data/2015-03-10 17-35-02.csv",
        "./data/2015-01-24 09-31-21.csv",
        "./data/2015-03-15 13-38-29.csv"
    ]
    bumps_paths = [
        "./bumps/2015-03-10 17-35-02(bumps).csv",
        "./bumps/2015-01-24 09-31-21(bumps).csv",
        "./bumps/2015-03-15 13-38-29(bumps).csv"
    ]
    csv_results = [
        "./results/2015-03-10 17-35-02_result.csv",
        "./results/2015-01-24 09-31-21_result.csv",
        "./results/2015-03-15 13-38-29_result.csv"
    ]

    # data_paths = glob.glob("./data/*.csv")
    # bumps_paths = glob.glob("./bumps/*.csv")
    # csv_results = list()
    # for x in data_paths:
    #     csv_results.append(x.replace(".csv", "_result.csv").replace("data", "results"))

    for data_index in range(len(data_paths)):
        data = pandas.read_csv(data_paths[data_index], parse_dates=['Time'])
        bumps = pandas.read_csv(bumps_paths[data_index])

        # threshold for z-thresh: 1.2, z-diff: 3, stdev(Z): 0.25, g-zero: 0.8, mod-z-thresh: 4.3
        threshold = 3
        window_size = 50

        prev_time = time.perf_counter()
        # result = algorithms.z_thresh(data, threshold)
        result = algorithms.z_diff(data, threshold)
        # result = algorithms.stdev_alg(data, threshold, window_size)
        # result = algorithms.g_zero(data, threshold)
        # result = algorithms.mod_z_thresh(data, threshold)
        # result = algorithms.my_alg(data, window_size)
        # result = algorithms.f_thresh(data, window_size, 1, 1)
        realize_time = time.perf_counter()-prev_time
        print("Alg time: {0}".format(realize_time))

        grouped_possible_artefacts = helpers.group_duplicates(result, 20)
        prepare_results(grouped_possible_artefacts)
        print(data_paths[data_index])
        check_statistic(grouped_possible_artefacts, bumps, threshold)
        print("---------------------------------------------------------")

        grouped_possible_artefacts_df = pandas.DataFrame(grouped_possible_artefacts, columns=["Latitude", "Longitude"])
        grouped_possible_artefacts_df.to_csv(csv_results[data_index], index=False)


def prepare_results(grouped_possible_artefacts):
    surveys = []
    for artefact in grouped_possible_artefacts:
        surveys.append(
            {
                "lat": artefact[0],
                "lng": artefact[1]
            }
        )
    print(surveys)


if __name__ == '__main__':
    main()
