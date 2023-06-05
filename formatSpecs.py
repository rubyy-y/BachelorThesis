import os
import glob
import json

def update_json_file(file_path, props):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data.pop("config", None)
        data = {**props, **data}
        file.seek(0)
        json.dump(data, file, indent=3)
        file.truncate()

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


# get list of all JSON files in the directory
os.chdir("BachelorThesis/vis-dif/public/data")
json_files = glob.glob("*.json")

# loop over each file
for file in json_files:
    update_json_file(file, props)
    print(f"{file} has been reformatted.")