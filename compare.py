import os
import json

def compare(a_json, b_json):
    with open(a_json) as a, open(b_json) as b:
        a_vl = json.load(a)
        b_vl = json.load(b)

        # x and y values
        a_x = a_vl["encoding"]["x"]["field"]
        a_y = a_vl["encoding"]["y"]["field"]
        b_x = b_vl["encoding"]["x"]["field"]
        b_y = b_vl["encoding"]["y"]["field"]

        # datapoints (list of dicts)
        data_a = a_vl["datasets"][list(a_vl["datasets"].keys())[0]]
        data_b = b_vl["datasets"][list(b_vl["datasets"].keys())[0]]

        # statistical measures for bar plot placeholder
        min_ = float("inf")
        max_ = float("-inf")
        step = max(len(data_a), len(data_b))

        # save differences to list of dictionaries
        diffs = []

        # # barplot
        isBarplot = False
        if a_vl["mark"] == "bar" or b_vl["mark"] == "bar":
            isBarplot = True
        
        if isBarplot:
            # iterate through first file
            for dp_a in data_a:
                if dp_a[a_y] < min_:
                    min_ = dp_a[a_y]
                elif dp_a[a_y] > max_:
                    max_ = dp_a[a_y]

                identical = any(dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y] for dp_b in data_b)
                if not identical:
                    dp_a["from file"] = "1"
                    diffs.append(dp_a)

            # iterate through second file
            for dp_b in data_b:
                if dp_b[b_y] < min_:
                    min_ = dp_b[b_y]
                elif dp_b[b_y] > max_:
                    max_ = dp_b[b_y]

                identical = any(dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y] for dp_a in data_a)
                if not identical:
                    dp_b["from file"] = "2"
                    diffs.append(dp_b)

        # scatterplot
        else:
            # iterate through first file
            for dp_a in data_a:
                identical = any(dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y] for dp_b in data_b)
                if not identical:
                    dp_a["from file"] = "1"
                    diffs.append(dp_a)

            # iterate through second file
            for dp_b in data_b:
                identical = any(dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y] for dp_a in data_a)
                if not identical:
                    dp_b["from file"] = "2"
                    diffs.append(dp_b)

        # specs - mandatory
        hash_ = list(a_vl["datasets"].keys())[0]
        mark = a_vl["mark"]
        encoding = a_vl["encoding"]

        output_vl = {
            "width": "container",
            "height": "container",
            "background": None,
            "config": {
                "legend": {"labelColor": "#3a393f", "titleColor": "black"},
                "axis": {"gridColor": "black"},
                "axisX": {"labelColor": "#3a393f", "titleColor": "black"},
                "axisY": {"labelColor": "#3a393f", "titleColor": "black"}
            },
            "data": {
                "name": hash_
            },
            "mark": mark,
            "encoding": encoding,
            "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
            "datasets": {
                hash_: diffs
            }
        }

        # if barplot, make placeholder
        if isBarplot:
            output_vl["params"] = [{"name": "placeholder", 
                                    "bind": {"input": "range", 
                                             "min": min_, 
                                             "max": max_, 
                                             "step": step}}]
        output_vl["encoding"]["tooltip"].insert(0, {'field' : "from file"})
        
        fe = len('_source.json')    # length of file ending
        output_file = f"{a_json[:-fe]}_COMP_{b_json[:-fe]}.json"
        with open("comparisons/" + output_file, 'w') as out:
            json.dump(output_vl, out, indent=2)
    return None
        

# function to update specs
def update_json_file(file_path, props):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data.pop("config", None)
        data = {**props, **data}
        file.seek(0)
        json.dump(data, file, indent=3)
        file.truncate()

# compare all the files in the data folder of our app-directory
os.chdir("BachelorThesis/vis-dif/public/data")

percent = [5, 10, 15, 20]
datasets = ["barley", "burtin", 
            "cars", "crimea", "driving", 
            "iris", "ohlc", "wheat"]

# Reformat specs
props = {
    "width": "container",
    "height": "container",
    "background": None,
    "config": {
        "legend": {"labelColor": "#3a393f", "titleColor": "black"},
        "axis": {"gridColor": "black"},
        "axisX": {"labelColor": "#3a393f", "titleColor": "black"},
        "axisY": {"labelColor": "#3a393f", "titleColor": "black"}
    }
}


if __name__ == "__main__":
    for dataset in datasets:
        original = f"{dataset}_source.json"
        for p in percent:
            alternation = f"{dataset}{p}_source.json"
            new_file = f"{dataset}_COMP_{dataset}{p}.json"

            print(f"\n{original} and {alternation}: ")
            try:
                compare(original, alternation)
                print("compared,")
                update_json_file("comparisons/"+new_file, props)
                print(f"new file {new_file} has been reformatted.")

            except:
                print("!! error")