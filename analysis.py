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

        # config = source['config']
        # data = source['data']
        # mark = source['mark']
        # schema = source['$schema']

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


def point_compare(a, b):
    """
    This function takes two DATAPOINTS as input
    and compares them
    """
    pass


def compare(a, b):
    """
    This function takes two JSON files as input
    and outputs general statistics and distinct datapoints that differ
    output should also be in JSON format to be able to plot
    """
    with open(a, 'r') as a:
        with open(b, 'r') as b:
            a_data = json.load(a)
            b_data = json.load(b)

            a_datasets = a_data["datasets"]
            b_datasets = b_data["datasets"]

            name_a = list(a_datasets.keys())
            name_b = list(b_datasets.keys())
            if not (len(name_a) == 1 and len(name_b) == 1):
                raise ValueError
            
            dataset_a = a_datasets[name_a[0]]
            dataset_b = b_datasets[name_b[0]]
            
            for a in range(len(dataset_a)):
                for b in range(len(dataset_b)):
                    point_compare(a, b)


# statistics("itis_source.json")
# compare("iris_source.json", "iris20_source.json")
