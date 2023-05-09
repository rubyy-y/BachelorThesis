# import section
import os
import json


def statistics(a):
    """
    This function takes one JSON file as input
    and returns general statistics for the data:
        - n_datapoints: number of datapoints
        - density: from area of datapoints get "area/n_datapoints"
        - propotion of color encoding targets
    """
    stats = dict()
    with open(a, "r") as f:
        source = json.load(f)

        # encoding values
        encoding = source["encoding"]
        x_val = encoding["x"]["field"]
        y_val = encoding["y"]["field"]
        color_val = encoding["color"]["field"]

        # get number of datapoints
        datasets = source["datasets"]
        dset = list(datasets.keys())
        if not len(dset) == 1:
            raise ValueError
        
        dataset = datasets[dset[0]]
        n_datapoints = len(dataset)

        stats["n_datapoints"] = n_datapoints

        # traverse through source once and collect values in dict    
        # initialize values 
        stats["min_x"] = dataset[0][x_val]
        stats["min_y"] = dataset[0][y_val]
        stats["max_x"] = dataset[0][x_val]
        stats["max_y"] = dataset[0][y_val]

        for data in dataset:
            # print(data)
            if data[x_val] < stats["min_x"]:
                stats["min_x"] = data[x_val]

            elif data[x_val] > stats["max_x"]:
                stats["max_x"] = data[x_val]

            if data[y_val] < stats["min_y"]:
                stats["min_y"] = data[y_val]

            elif data[y_val] > stats["max_y"]:
                stats["max_y"] = data[y_val]

            # color
            try:
                stats[data[color_val]] += 1
            except KeyError:
                # if this key doesnt exist yet
                stats[data[color_val]] = 1

        # get density
        range_x = stats["max_x"] - stats["min_x"]
        range_y = stats["max_y"] - stats["min_y"]
        area = range_x * range_y
        
        stats["density"] = area/n_datapoints
        return stats


# def compare(a_json, b_json):
#     """
#     This function takes two JSON files as input
#     and outputs general statistics and distinct datapoints that differ
#     output should also be in JSON format to be able to plot
#     ... This only returns the datapoints which are in a but not in b
#     """
        
#     # dict to save values and information
#     summary = dict({"identical": 0})

#     with open(a_json, 'r') as a:
#         with open(b_json, 'r') as b:
#             a_data = json.load(a)
#             b_data = json.load(b)

#             # check if encoding labels are the same
#             a_encoding = a_data["encoding"]
#             b_encoding = b_data["encoding"]

#             a_x_val = a_encoding["x"]["field"]
#             a_y_val = a_encoding["y"]["field"]
#             a_color_val = a_encoding["color"]["field"]

#             b_x_val = b_encoding["x"]["field"]
#             b_y_val = b_encoding["y"]["field"]
#             b_color_val = b_encoding["color"]["field"]

#             summary["same_x"] = a_x_val == b_x_val
#             summary["same_y"] = a_y_val == b_y_val
#             summary["same_color"] = a_color_val == b_color_val

#             # comparing single datapoints
#             a_datasets = a_data["datasets"]
#             b_datasets = b_data["datasets"]

#             name_a = list(a_datasets.keys())
#             name_b = list(b_datasets.keys())
#             if not (len(name_a) == 1 and len(name_b) == 1):
#                 raise ValueError
            
#             dataset_a = a_datasets[name_a[0]]
#             dataset_b = b_datasets[name_b[0]]

#             # make new directory for comparing files
#             os.makedirs("comparisons", exist_ok=True)

#             # create file to add non identical datapoints
#             comp = f"{a_json[:-(len('_source.json'))]}_COMP_{b_json[:-(len('_source.json'))]}.json"

#             with open(f"comparisons\{comp}", 'wb') as comp:
#                 comp.write(bytes("[\n", 'utf-8'))
#                 for a_point in dataset_a:
#                     for b_point in dataset_b:
#                         if a_point == b_point:
#                             summary["identical"] += 1

#                     if not a_point in dataset_b:
#                         string = str(a_point)
#                         string = string.replace("'", "\"").replace("None", "null")
#                         comp.write(bytes(f"\t{string},\n", 'utf-8'))
                
#                 # delete last comma
#                 comp.seek(-2, 2)
#                 comp.truncate()

#                 comp.write(bytes("\n]", 'utf-8'))
#     return summary

def compare(a_json, b_json):
    with open(a_json) as a, open(b_json) as b:
        # length of file ending ("_source.json")
        fe = len('_source.json')
        output_file = f"{a_json[:-fe]}_COMP_{b_json[:-fe]}.json"

        a_vl = json.load(a)
        b_vl = json.load(b)

        # x and y values
        a_x = a_vl["encoding"]["x"]["field"]
        a_y = a_vl["encoding"]["y"]["field"]
        b_x = b_vl["encoding"]["x"]["field"]
        b_y = b_vl["encoding"]["y"]["field"]

        # datapoints (list of dicts)
        data_a = a_vl["datasets"]
        hash_a = list(data_a.keys())[0]
        data_a = a_vl["datasets"][hash_a]

        data_b = b_vl["datasets"]
        hash_b = list(data_b.keys())[0]
        data_b = b_vl["datasets"][hash_b]

        # save differences to list of dictionaries
        diffs = []
        diffs_files = []    # differences with additional file feature

        # iterate through first file
        for dp_a in data_a:
            identical = False
            for dp_b in data_b:
                if dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y]:
                    identical = True
                    break
            if not identical:
                diffs.append(dp_a)
                dp_a["file of origin"] = "File 1"
                diffs_files.append(dp_a)

        # iterate through second file
        for dp_b in data_b:
            identical = False
            for dp_a in data_a:
                if dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y]:
                    identical = True
                    break
            if not identical:
                diffs.append(dp_b)
                dp_b["file of origin"] = "File 2"
                diffs_files.append(dp_b)

        # specs - mandatory
        hash_ = hash_a
        mark = a_vl["mark"]
        encoding = a_vl["encoding"]
        encoding["color"]["field"] = "file of origin"
        encoding["color"]["type"] = "nominal"

        output_vl = {
            "width": "container",
            "height": "container",
            "background": "white",
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

        # specs - optional
        # selector
        try:
            selection = a_vl["selection"]
            output_vl["selection"] = selection
        except:
            pass

        with open("comparisons/" + output_file, 'w') as out:
            json.dump(output_vl, out, indent=3)


# compare all the files in the data folder of our app-directory
os.chdir("BachelorThesis/vis-dif/public/data")
# compare("iris_source.json", "iris20_source.json")

datasets = ["anscombe", "barley", "burtin", 
            "cars", "crimea", "driving", 
            "iris", "ohlc", "wheat"]

# datasets = ["burtin", 
#             "cars", "crimea", "driving", 
#             "iris", "wheat"]
percent = [20]

for dataset in datasets:
    print(dataset+": ")
    if dataset+"_source.json" in os.listdir():
        original = f"{dataset}_source.json"
        for p in percent:
            if dataset+str(p)+"_source.json" in os.listdir():
                alternation = f"{dataset+str(p)}_source.json"
                try:
                    compare(original, alternation)
                    print("successful\n")
                except:
                    print("!! unsuccessful\n")


# main call not needed because this is a utility function, used in backend
# if __name__ == "__name__":
#     pass
