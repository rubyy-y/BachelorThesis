# import section
import os
import json

try:
    os.chdir("BachelorThesis\datasets\sources")
except:
    pass


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


def compare(a_json, b_json):
    """
    This function takes two JSON files as input
    and outputs general statistics and distinct datapoints that differ
    output should also be in JSON format to be able to plot
    ... This only returns the datapoints which are in a but not in b
    """
        
    # dict to save values and information
    summary = dict({"identical": 0})

    with open(a_json, 'r') as a:
        with open(b_json, 'r') as b:
            a_data = json.load(a)
            b_data = json.load(b)

            # check if encoding labels are the same
            a_encoding = a_data["encoding"]
            b_encoding = b_data["encoding"]

            a_x_val = a_encoding["x"]["field"]
            a_y_val = a_encoding["y"]["field"]
            a_color_val = a_encoding["color"]["field"]

            b_x_val = b_encoding["x"]["field"]
            b_y_val = b_encoding["y"]["field"]
            b_color_val = b_encoding["color"]["field"]

            summary["same_x"] = a_x_val == b_x_val
            summary["same_y"] = a_y_val == b_y_val
            summary["same_color"] = a_color_val == b_color_val

            # comparing single datapoints
            a_datasets = a_data["datasets"]
            b_datasets = b_data["datasets"]

            name_a = list(a_datasets.keys())
            name_b = list(b_datasets.keys())
            if not (len(name_a) == 1 and len(name_b) == 1):
                raise ValueError
            
            dataset_a = a_datasets[name_a[0]]
            dataset_b = b_datasets[name_b[0]]

            # make new directory for comparing files
            os.makedirs("comparisons", exist_ok=True)

            # create file to add non identical datapoints
            comp = f"{a_json[:-(len('_source.json'))]}_COMP_{b_json[:-(len('_source.json'))]}.json"

            # opening file in byte mode
            # else seek operation not available
            with open(f"comparisons\{comp}", 'wb') as comp:
                comp.write(bytes("[\n", 'utf-8'))
                for a_point in dataset_a:
                    for b_point in dataset_b:
                        if a_point == b_point:
                            summary["identical"] += 1

                    if not a_point in dataset_b:
                        string = str(a_point)
                        string = string.replace("'", "\"").replace("None", "null")
                        comp.write(bytes(f"\t{string},\n", 'utf-8'))
                
                # delete last comma
                comp.seek(-2, 2)
                comp.truncate()

                comp.write(bytes("\n]", 'utf-8'))
    return summary

# compare("iris_source.json", "iris20_source.json")
# compare("iris20_source.json", "iris_source.json")


# main call not needed because this is a utility function, used in backend
# if __name__ == "__name__":
#     pass
    # for i in ...:
    #     compare("iris_source.json", "iris20_source.json")

