import os
import shutil
import pandas as pd
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import Metadata

def parse_data(file_name):
    output_fp = open("wine_data.csv", "a")

    count = 0
    with open(file_name, "r") as fp:
        line = fp.readline().strip()

        while line:
            if line.startswith("type") or line.startswith("\"fixed") or line.startswith("fixed"):
                line =  fp.readline().strip()
                continue

            if ";" in line:
                data = line.split(";")
            else:
                data = line.split(",")

            if len(data) == 13:
                print(",".join(data[1:]))
                output_fp.write(",".join(data[1:]) + "\n")
            else:
                print(",".join(data))
                output_fp.write(",".join(data) + "\n")

            count = count + 1
            line = fp.readline().strip()

    output_fp.close()

    return count

def recreate_data_file():
    if os.path.exists('wine_data.csv'):
        os.remove('wine_data.csv')
        shutil.copyfile('wine_data.csv.bak', 'wine_data.csv')

def synth_data(synth_count):
    # remove file then re-generate it
    if os.path.exists('synthetic_wine_data.csv'):
        os.remove('synthetic_wine_data.csv')

    real_data = pd.read_csv('wine_data.csv')

    # load metadata if exists
    if os.path.exists('synthetic_metadata.json'):
        metadata = Metadata.load_from_json(filepath = 'synthetic_metadata.json')
    else:
        metadata = Metadata.detect_from_dataframe(data = real_data)
        metadata.save_to_json(filepath = 'synthetic_metadata.json')

    # Create and fit the synthesizer model
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(real_data)
    synthetic_data = synthesizer.sample(num_rows = synth_count)

    # Save synthetic data
    synthetic_data.to_csv('synthetic_wine_data.csv', index = False)


def main():
    # this script should only be run once but here is the handling if run multiple times
    recreate_data_file()

    c = 0
    c = c + parse_data("winequalityN.csv")
    c = c + parse_data("winequality-red.csv")
    c = c + parse_data("winequality-white.csv")

    synth_data(20000)

    c = c + parse_data("synthetic_wine_data.csv")

    print("total lines are added: {}".format(c))

if __name__ == "__main__":
    main()