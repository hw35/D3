import csv
import json
import pandas as pd
import numpy as np

dictionary = {}
expArray = []
df=pd.read_csv("RETTLdata.csv")
expArray=df["MappedExpertise"]

#expArray = [item['MappedExpertise'] for item in data1]
i = 0
while i < len(expArray):
    tempArr = str(expArray[i]).split(",")
    j = 0
    while j < len(tempArr):
        cur = tempArr[j]
        cur = cur.strip()
        if " " in cur:
            first = cur.split(" ")[0]
            rest = cur[len(first):].lower()
            cur = first + rest
        if cur not in dictionary:
            dictionary[cur] = 1
        else:
            dictionary[cur] += 1
        j += 1
    i += 1
    
# helper to create dict of dict of .. of values
def add_leaf(tree, row):
    key = row[0]
    #print(key)
    #print(row[1:])
    if len(row) > 2:
        if not key in tree:
            tree[key] = {}
        add_leaf(tree[key], row[1:])
    if len(row) == 2:
            tree[key] = row[1]

# transforms helper structure to final structure
def transform_tree(tree):
    res = []
    res_entry = []
    for key, val in tree.items():
        if isinstance(val, dict):
            if(key in dictionary):
                res.append({
                    "name": key,
                    #"size": val,
                    
                    "value":dictionary[key],
                    "children": transform_tree(val),
                    })
            else:
                res.append({
                    "name": key,
                    #"size": val,
                    "children": transform_tree(val),
                    })
        else:
            res.append({
                "name": key,
                #"shortName": key,
                #"children": transform_tree(val),
                })
    return res
def main():
    """ The main thread composed from two parts.

    First it's parsing the csv file and builds a tree hierarchy from it.
    It uses the recursive function add_leaf for it.

    Second it's recursively transforms this tree structure into the
    desired hierarchy

    And the last part is just printing the result.

    """
    f=open("makeTree2.json","w")
    # Part1 create a hierarchival dict of dicts of dicts.
    # The leaf cells are however just the last element of each row
    tree = {}
    with open('mappedE_Actor.csv') as csvfile:
        reader = csv.reader(csvfile)
        for rid, row in enumerate(reader):
            if rid == 0:  # skip header row
                continue
            add_leaf(tree, row)

    # uncomment to visualize the intermediate result
    # print(json.dumps(tree, indent=1))
    # print("=" * 76)

    # transfor the tree into the desired structure
    res = transform_tree(tree)
    f.write(json.dumps(res, indent=1))

# so let's roll
main()