import os
from pathlib import Path
import csv
import io


root_dir = Path(__file__).parent.parent
data_dpath = os.path.join(root_dir, "data", "keys")


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


# with open("output.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerows(data)

# ╰─ for key in $(cat data/MS_FLASCQ.txt); do found_in_core=$(grep -q $key data/MS_SCQ.txt); found_in_ft=$(grep -q $key data/FT_FLASCQ.txt); if [[ "$found_in_ft" == false && "$found_in_core" == true ]]; then "key comes from core"; fi; done


def generate_csv(data):
    # create an in-memory text stream
    output = io.StringIO()
    # create a CSV writer object
    writer = csv.writer(output)
    # write data to the CSV
    writer.writerows(data)
    # get the CSV string from the in-memory text stream
    csv_output = output.getvalue()
    # Print the CSV output
    print(csv_output)

    # Close the in-memory text stream
    output.close()


if __name__ == "__main__":
    data = []
    file_list = list_files(data_dpath)
    ms_keys = read_files(
        [file for file in file_list if file.startswith("MS_")], data_dpath
    )
    ft_keys = read_files(
        [file for file in file_list if file.startswith("FT_")], data_dpath
    )

    for unit in ms_keys.keys():
        if (
            unit.startswith("FLA")
            and not unit.endswith("INT")
            and unit in ft_keys.keys()
        ):
            for key in ms_keys[unit]:
                core_unit = unit.replace("FLA", "", 1)
                cores = ["STQ", "SCQ", "PAQ", "TCQ", "ICQ"]
                if core_unit not in cores:
                    print(f"Core unit {core_unit} not in cores")
                if key not in ft_keys[unit] and key in ms_keys[core_unit]:
                    # print(f"Key '{key}' in FLA{core_unit} came from {core_unit}")
                    print(f"{core_unit},{unit},{key}")
                    data.append([core_unit, unit, key])

    generate_csv(data)

    with open("output.csv", "w", newline="\n") as file:
        writer = csv.writer(file)
        writer.writerows(data)
