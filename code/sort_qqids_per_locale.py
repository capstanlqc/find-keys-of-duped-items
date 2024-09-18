import os
import pandas as pd


root_dir = Path(__file__).parent.parent
file_path = os.path.join(root_dir, "data", "ft-twms-qq-mask.csv")
units = ["FLAPAQ", "FLASCQ", "FLASTQ", "FLATCQ", "ICQ", "LDWSTQ", "PAQ", "SCQ", "STQ", "TCQ", "FLATCQSCI"]
data = {}

with open(file_path, "r", encoding="utf-8") as file:
    lines = file.read().splitlines()

for line in lines:
	unit_list = line.split(",")
	masks = {}
	for unit in units:
		if unit == "FLATCQSCI" and "FLATCQ" in unit_list and "TCQ" in unit_list:
			masks[unit] = "Y"
		elif unit in unit_list:
			masks[unit] = "Y"
		else:
			masks[unit] = "N"
	locale = unit_list[0]
	data[locale] = masks

df = pd.DataFrame.from_dict(data, orient='index')
# reset the index to have 'locale' as a column
df = df.reset_index().rename(columns={'index': 'locale'})

# save df in three formats
df.to_csv('output/qq_masks_bool.csv', index=False)
df.to_excel('output/qq_masks_bool.xlsx', index=False)
df.to_json('output/qq_masks_bool.json', orient='records', indent=4)
