import csv
import json

# helper to create dict of dict of .. of values
def add_leaf(tree, row):
    key = row[0]
    if len(row) > 2:
        if not key in tree:
            tree[key] = {}
        add_leaf(tree[key], row[1:])
    if len(row) == 2:
            tree[key] = row[-1]

# transforms helper structure to final structure
def transform_tree(tree):
    res = []
    res_entry = []
    for key, val in tree.items():
        if isinstance(val, dict):
            res.append({
                "name": key,
                #"shortName": key,
                #"size":val,
                })
        else:
            res.append({
                "name": key,
                "size":val,
                #"shortName": key,
                "children": transform_tree(val),
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