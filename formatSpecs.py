# imports
import os
import json

# navigate to source files
os.chdir("BachelorThesis/vis-dif/public/data")

datasets = ["barley", "burtin", 
            "cars", "crimea", "driving", 
            "iris", "ohlc", "wheat"]

props = {
    "width": "container",
    "height": "container",
    "background": None,
    "config": {
        "legend": {"labelColor": "white", "titleColor": "white"},
        "axis": {"gridColor": "white"},
        "axisX": {"labelColor": "white", "titleColor": "white"},
        "axisY": {"labelColor": "white", "titleColor": "white"}
            }
}

for dataset in datasets:
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
    percentages = [5, 10, 15, 20]
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