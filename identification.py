"""
This file takes a dataset and adds an ID to each datapoint.
Afterwards, the dataset needs to be randomized.
"""

import os
os.chdir("BachelorThesis/datasets")

import json
# dataset = "iris.json"
dataset = input("input dataset name: ") + ".json"
id_data = []

with open(dataset) as f:
    data = json.load(f)
    _id = 1

    for dp in data:
        dp["_ID_"] = _id
        _id += 1

        id_data.append(dp)

# os.chdir("../vis-dif/public/data/id_datasets")
with open("id_datasets/[id]_" + dataset, "x") as n:
    json.dump(id_data, n, indent=2)