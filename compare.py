import os
import json

with open("globals.json") as globs:
    globals = json.load(globs)

id_sets = globals["ID_datasets"]
props = globals["VL"]

def compare(a_json, b_json):
    with open(a_json) as a, open(b_json) as b:
        a_vl = json.load(a)
        b_vl = json.load(b)

        # x and y, color values
        a_x = a_vl["encoding"]["x"]["field"]
        a_y = a_vl["encoding"]["y"]["field"]

        b_x = b_vl["encoding"]["x"]["field"]
        b_y = b_vl["encoding"]["y"]["field"]

        color = a_vl["encoding"]["color"]["field"]

        # datapoints (list of dicts)
        data_a = a_vl["datasets"][list(a_vl["datasets"].keys())[0]]
        data_b = b_vl["datasets"][list(b_vl["datasets"].keys())[0]]

        # save differences to list of dictionaries
        diffs = []

        # Barplot
        mark = a_vl["mark"]
        if mark == "bar":
            # find identicals, regardless of y value
            for dp_a in data_a:
                identical = False
                for dp_b in data_b:
                    if all(dp_a[key] == dp_b[key] for key in [a_x, color]):
                        identical = True

                        difference = dp_a[a_y] - dp_b[b_y]
                        dif = dp_a.copy()
                        dif[a_y] = difference

                        if difference < 0:
                            dif["from file"] = "added to alternation"
                        elif difference > 0:
                            dif["from file"] = "removed from original"

                        diffs.append(dif)
                        break

                if not identical:   # point was removed
                    dp_a["from file"] = "original"
                    dp_a[a_y] *= -1
                    diffs.append(dp_a)

            
            # search dor dp in b not in a
            for dp_b in data_b:
                identical = False
                for dp_a in data_a:
                    if all(dp_a[key] == dp_b[key] for key in [a_x, color]):
                        identical = True
                        break

                if not identical:
                    dp_b["from file"] = "alternation"
                    diffs.append(dp_b)

        # Scatterplot
        else:
            # iterate through first file
            for dp_a in data_a:
                identical = any(dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y] for dp_b in data_b)
                if not identical:
                    dp_a["from file"] = "original"
                    diffs.append(dp_a)

            # iterate through second file
            for dp_b in data_b:
                identical = any(dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y] for dp_a in data_a)
                if not identical:
                    dp_b["from file"] = "alternation"
                    diffs.append(dp_b)

        # Make new specification
        hash_ = list(a_vl["datasets"].keys())[0]
        mark = a_vl["mark"]
        encoding = a_vl["encoding"]

        output_vl = props.copy()
        output_vl["data"] = { "name": hash_ }
        output_vl["mark"] = mark
        output_vl["encoding"] = encoding
        output_vl["$schema"] = "https://vega.github.io/schema/vega-lite/v4.17.0.json"
        output_vl["datasets"] = { hash_: diffs }

        # if mark == "bar":
        #     ranges = [dif[a_y] for dif in diffs]
        #     min_ = min(ranges)-(min(ranges)*0.5)
        #     max_ = max(ranges)+(max(ranges)*0.5)
        #     output_vl["encoding"]["y"]["scale"] = {"domain": [-max(ranges), max(ranges)]}

        output_vl["encoding"]["tooltip"].insert(0, {'field' : "from file"})
        
        fe = len('_source.json')    # length of file ending
        output_file = f"{a_json[:-fe]}_COMP_{b_json[:-fe]}.json"
        with open("comparisons/" + output_file, 'w') as out:
            json.dump(output_vl, out, indent=2)

    return None  


def id_compare(a_json, b_json):
    """
    This function compares datasets in case they have an ID feature.
    """
    with open(a_json) as a, open(b_json) as b:
        a_vl = json.load(a)
        b_vl = json.load(b)

        # datapoints (list of dicts)
        data_a = a_vl["datasets"][list(a_vl["datasets"].keys())[0]]
        data_b = b_vl["datasets"][list(b_vl["datasets"].keys())[0]]

        for dp_a in data_a:
            _id_ = dp_a["_ID_"]
            exists = False

            for dp_b in data_b:
                if dp_b["_ID_"] == _id_:
                    exists = True
                if exists:
                    print(dp_a, "\n", dp_b)
                    break

    return None


# __________U__P__D__A__T__E_____S__P__E__C__S__________
def update_json_file(file_path, props):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        data.pop("config", None)
        data = {**props, **data}
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()

# compare all the files in the data folder of our app-directory
os.chdir("vis-dif/public/data")

percent = globals["percent"]
datasets = globals["datasets"]


id_compare("cars_source.json", "cars20_source.json")


# if __name__ == "__main__":
#     for dataset in datasets:
#         original = f"{dataset}_source.json"
#         update_json_file(original, props)
#         for p in percent:
#             alternation = f"{dataset}{p}_source.json"
#             update_json_file(alternation, props)    # reformat alternation vis
#             new_file = f"{dataset}_COMP_{dataset}{p}.json"

#             print(f"\nComparing {original} and {alternation}: ")
#             try:
#                 if dataset in id_sets:
#                     print("This is a dataset with ID values.")
#                     id_compare(original, alternation)
#                 else:
#                     compare(original, alternation)
#                     update_json_file("comparisons/" + new_file, props)
#                     print(f"new file {new_file} has been reformatted.")

#             except:
#                 raise Warning