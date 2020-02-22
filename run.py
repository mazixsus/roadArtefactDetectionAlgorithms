import sys
import pandas
import z_thresh
import helper_scripts.helpers as helpers


def get_data(data_paths):
    data_paths = list()
    bumps_paths = list()
    csv_results = list()
    data_paths.append("./data/2015-03-10 17-35-02.csv", )


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
    data_paths = ["./data/2015-03-10 17-35-02.csv", "./data/2015-01-24 09-31-21.csv", "./data/2015-03-15 13-38-29.csv"]
    bumps_paths = ["./data/2015-03-10 17-35-02(bumps).csv", "./data/2015-01-24 09-31-21(bumps).csv",
                   "./data/2015-03-15 13-38-29(bumps).csv"]
    csv_results = ["./results/2015-03-10 17-35-02_result.csv", "./results/2015-01-24 09-31-21_result.csv",
                   "./results/2015-03-15 13-38-29_result.csv"]

    for data_index in range(len(data_paths)):
        data = pandas.read_csv(data_paths[data_index], parse_dates=['Time'])
        bumps = pandas.read_csv(bumps_paths[data_index])

        threshold = 1.2
        result = z_thresh.z_thresh(data, threshold)
        check_statistic(result, bumps, threshold)

        result = pandas.DataFrame(result, columns=["Latitude", "Longitude"])
        result.to_csv(csv_results[data_index], index=False)


if __name__ == '__main__':
    main()
