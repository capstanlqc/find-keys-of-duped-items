# Find keys of relocated items

The purpose of this utility is to extract the list of keys which were used in a certain questoinnaire in FT and have now been copied in MS to other related files.

## Extract data

To collect the necessary data, extract the keys from each XML file. 

For each cycle (FT and MS), do the following: 

1. Change directory to the repository containing the `source` folder.

```
cd /path/to/common
```

2. Run the script to extract keys from all XML files inside QQ batch folders: 

```
bash /path/to/find-keys-of-duped-items/code/extract_keys.sh
```
<!-- 
for f in $(find source/0?_QQ?_N -name "*.xml"); do id=$(echo $(basename $f) | cut -d"_" -f4 | cut -d"-" -f1); echo $id; echo $f; grep -Poh --color '(?<=<label key=")[^"]+(?=")' $f > ../../ACER-PISA-2025-MS/keys/PISA2025FT_$id.txt; done
-->

3. Rename output files to tag them with the cycle:

```
# cycle is either 'FT' or 'MS', e.g. 
perl-rename 's/^/MS_/' *.txt
perl-rename 's/^/FT_/' *.txt
```

4. Finally, move the keys files for both cycles to `data/keys` in this repo.

## Run the three-side comparison

Run the following script to extract the keys that have been copied to another QQ file in MS:

```
python code/find_keys_of_relocated_items.py
```