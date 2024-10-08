import os
from pathlib import Path
import csv
from datetime import datetime
from rich import print
import pandas as pd

root_dir = Path(__file__).parent.parent
data_dpath = os.path.join(root_dir, "data", "keys")
transfer_fpath = os.path.join(root_dir, "data", "pisa_qq_ft2ms_item_mapping.csv")

today = datetime.today()
formatted_date = today.strftime("%Y%m%d")


def read_csv_file(fpath):
    with open(fpath, mode="r") as file:
        return [row for row in csv.DictReader(file)]


def merge_entries_with_same_key(df):
    return (
        df.groupby("FT")["MS"]
        .apply(lambda x: " ".join(sorted(set(" ".join(x).split()))))
        .reset_index()
    )


def csv_to_dict(csv_data):
    df = pd.DataFrame.from_dict(csv_data)
    df_merged = merge_entries_with_same_key(df)
    # return dict(zip(df_merged["FT"], df_merged["MS"])) # equivalent to
    return df_merged.set_index("FT")["MS"].to_dict()


def get_unit_mapping(csv_data):
    return {
        ft_unit: [unit for unit in ms_units.split() if unit != ft_unit]
        for ft_unit, ms_units in csv_to_dict(csv_data).items()
    }


def list_files(directory):
    files = os.listdir(directory)
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    return files


def read_files(file_list, data_dpath):
    contents = {}

    for file_name in file_list:
        file_path = os.path.join(data_dpath, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                # Read the content of the file
                lines = file.read().splitlines()
                # Store the content in a dictionary with the file name as the key
                unit = Path(file_name).stem.split("_")[1]
                contents[unit] = lines
                # print(f"Read {file_name} successfully.")
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")

    return contents


def get_files_containing_key(key, keys_in_files):
    files_with_value = [k for k, values in keys_in_files.items() if key in values]
    return files_with_value


def get_keys_in_files_for_cycle(cycle, data_dpath):
    return read_files(
        [file for file in file_list if file.startswith(f"{cycle}_")], data_dpath
    )


if __name__ != "__main__":
    exit()

# collect some data first

data = []
csv_data = read_csv_file(transfer_fpath)
mapping = get_unit_mapping(csv_data)

ft_units = mapping.keys()
file_list = list_files(data_dpath)

# XX_ stands for three characters: either FT_ or MS_
qq_units = set([file[len("XX_") :][: -len(".txt")] for file in file_list])
units_not_extracted = [unit for unit in ft_units if unit not in qq_units]

if len(units_not_extracted) != 0:
    exit(f"Check unit IDs and try again: {",".join(units_not_extracted)}")

for unit in ft_units:
    print(
        f"Find keys in FT's '{unit}' which are now in any of '{",".join(mapping[unit])}' in MS"
    )

keys_in_ft_files = get_keys_in_files_for_cycle("FT", data_dpath)
keys_in_ms_files = get_keys_in_files_for_cycle("MS", data_dpath)

# find relocated units

for ft_unit in ft_units:
    if ft_unit not in keys_in_ft_files.keys():
        print(f"Unit {ft_unit} not found in FT files")
        continue

    for key in keys_in_ft_files[ft_unit]:
        keys_in_mapped_files = {
            k: keys_in_ms_files[k] for k in mapping[ft_unit] if k in keys_in_ms_files
        }
        ms_units = get_files_containing_key(key, keys_in_mapped_files)

        # print(f"{key} found in {",".join(ms_units)}")
        for ms_unit in ms_units:
            data.append([ft_unit, ms_unit, key])

# generate results

output_dir = f"output/{formatted_date}"
os.makedirs(output_dir, exist_ok=True)
results_file = f"{output_dir}/keys_{formatted_date}.csv"
with open(results_file, "w", newline="\n") as file:
    writer = csv.writer(file)
    writer.writerows(sorted(data))
