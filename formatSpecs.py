# This file will be needed to transform the json files;
# the compiles vega does not offer the needed specs to implement in the file
# example: container heigt
    # original json says "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}}
    # but we need "height": "container"
    #             "width": "container"
# also "background": null

# This file will also combine two comparisions
# and remove the click actions button

# for each souce file of the same dataset, specs are the same, but datahash and data, duh..

# we compare the source files
# __________________________________________________________________________________________

# imports
import os
import glob
import json

# navigate to source files
try:
    os.chdir("BachelorThesis/vis-dif/public/data")
except:
    pass

datasets = ["anscombe", "barley", "burtin", 
            "cars", "crimea", "driving", 
            "iris", "ohlc", "wheat"]

# for dataset in datasets:
#     print(f"Dataset: {dataset}")
#     with open(f"{dataset}_source.json", 'r') as f:
#         data = json.load(f)
#         print(data.keys(), '\n')

# instead of config, we want width, height and background

# datasets = ["TEST"]

props = {"width": "container",
         "height": "container",
         "background": None}

for dataset in datasets:
    # print(f"Dataset: {dataset}")
    data = None
    with open(f"{dataset}_source.json") as f:
        data = json.load(f)
  
    # edit data: remove config, add props
    try:
        data.pop("config", None)
    except KeyError:
        pass
    data = {**props, **data}

    # replace in file
    with open(f"{dataset}_source.json", 'w') as f:
        json.dump(data, f, indent=3)
        print(f"{dataset}_source.json has been reformatted.")

    # ALTERNATIONS
    percentages = [20]
    for percent in percentages:
        data = None
        with open(f"{dataset}{percent}_source.json") as a:
            data = json.load(a)
        
        try:
            data.pop("config", None)
        except KeyError:
            pass
        data = {**props, **data}

        with open(f"{dataset}{percent}_source.json", 'w') as a:
            json.dump(data, a, indent=3)
            print(f"{dataset}{percent}_source.json has been reformatted.")