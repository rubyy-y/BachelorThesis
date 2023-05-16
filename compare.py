# import section
import os
import json

def compare(a_json, b_json):
    print(a_json, "and", b_json)

    with open(a_json) as a, open(b_json) as b:
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
        
        # iterate through first file
        for dp_a in data_a:
            identical = False
            for dp_b in data_b:
                if dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y]:
                    identical = True
                    break
            if not identical:
                dp_a["from file"] = "1"
                diffs.append(dp_a)

        # iterate through second file
        for dp_b in data_b:
            identical = False
            for dp_a in data_a:
                if dp_a[a_x] == dp_b[b_x] and dp_a[a_y] == dp_b[b_y]:
                    identical = True
                    break
            if not identical:
                dp_b["from file"] = "2"
                diffs.append(dp_b)

        # specs - mandatory
        hash_ = hash_a
        mark = a_vl["mark"]
        encoding = a_vl["encoding"]
        encoding["color"]["legend"] = None

        output_vl = {
            "width": "container",
            "height": "container",
            "background": None,
            "config": {
                "axis": {"gridColor": "white"},
                "axisX": {"labelColor": "white", "titleColor": "white"},
                "axisY": {"labelColor": "white", "titleColor": "white"}
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

        # specs - optional selector
        try:
            selection = a_vl["selection"]
            output_vl["selection"] = selection
        except:
            pass

        # save with file coloring
        fe = len('_source.json')    # length of file ending
        output_file = f"{a_json[:-fe]}_COMP_{b_json[:-fe]}.json"
        with open("comparisons/" + output_file, 'w') as out:
            json.dump(output_vl, out, indent=3)

        # save with file color encoding
        output_vl["encoding"]["color"]["legend"] = None
        output_vl["encoding"]["color"]["field"] = "from file"
        output_vl["encoding"]["color"]["type"] = "nominal"
        output_vl["encoding"]["color"]["scale"] = {
            "domain": ["1", "2"],
            "range": ["lightblue", "gold"]
        }
        output_vl["encoding"]["tooltip"].insert(0, {'field' : "from file"})    
        # print(output_vl["encoding"]["tooltip"])  

        with open("comparisons/filecolor/" + output_file, 'w') as out:
            json.dump(output_vl, out, indent=3)

        print("successful\n")
        

# compare all the files in the data folder of our app-directory
os.chdir("BachelorThesis/vis-dif/public/data")

datasets = ["barley", "burtin", 
            "cars", "crimea", "driving", 
            "iris", "ohlc", "wheat"]

percent = [5, 10, 15, 20]

for dataset in datasets:
    print(dataset+": ")
    if dataset+"_source.json" in os.listdir():
        original = f"{dataset}_source.json"
        for p in percent:
            if dataset+str(p)+"_source.json" in os.listdir():
                alternation = f"{dataset+str(p)}_source.json"
                try:
                    compare(original, alternation)
                except:
                    print("!! unsuccessful\n")

# main call not needed because this is a utility function, used in backend
# if __name__ == "__name__":
#     pass
