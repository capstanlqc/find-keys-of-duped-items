# Find keys of relocated items

The purpose of this utility is to extract the list of keys which were and are used in a core questoinnaire (e.g. STQ, SCQ, PAQ, TCQ, ICQ) which have been copied in MS to the FLA counterpart of a core questionnaire but were not in the same FLA unit in FT.

## Getting started

To collect the necessary data, extract the keys from each XML file. 

For each cycle (FT and MS), do the following: 

1. Change directory to the repository containing the `source` folder.

```
cd /path/to/common
```

2. Run the script to extract keys from all XML files inside QQ batch folders: 

```
bash /run/media/souto/257-FLASH/dev/find-keys-of-duped-items/code/extract_keys.sh
```
<!-- 
for f in $(find source/0?_QQ?_N -name "*.xml"); do id=$(echo $(basename $f) | cut -d"_" -f4 | cut -d"-" -f1); echo $id; echo $f; grep -Poh --color '(?<=<label key=")[^"]+(?=")' $f > ../../ACER-PISA-2025-MS/keys/PISA2025FT_$id.txt; done
-->

3. Rename output files to tag them with the cycle:

```
# cicle is either 'FT' or 'MS'
perl-rename 's/^/MS_/' *.txt
```

4. Finally, move the keys files for both cycles to `data/keys` in this directory

## Run the three-side comparison

Run the following script to list the keys that have been copied to a FLA quesitonnaire in MS:

```
python code/find_keys_of_relocated_items.py
```