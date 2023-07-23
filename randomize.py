# import section
import os
import glob
import json
import random
random.seed(10)

# change path to where json files are
os.chdir("BachelorThesis\datasets")
json_files = os.getcwd() + "\*.json"

# scan for all .json files in this folder
files = [os.path.split(file)[-1] for file in glob.glob(json_files)]

# ________________________________________________________________________________
def toChange(file):
    """
    file: json source file
    returns a list of the encoding fields that are NOT x or color of the spec.
    """
    with open("../vis-dif/public/data/" + file) as f:
        f_vl = json.load(f)
        keys = list(f_vl["datasets"][list(f_vl["datasets"].keys())[0]][0].keys())
        
        keys.remove(f_vl["encoding"]["x"]["field"])
        keys.remove(f_vl["encoding"]["color"]["field"])
        keys.remove("_ID_")
        return keys
    
def statistics(data):
    """
    input: datapoints as list of dicts
    output: min max value of int/float and list of values of strings
    """
    values = {}
    for dp in data:
        for key in dp:
            if isinstance(dp[key], (int, float)) and key != "_ID_":
                if key+"_min" not in values:
                    values[key+"_min"] = dp[key]
                elif key+"_max" not in values:
                    values[key+"_max"] = dp[key]
                else:
                    values[key+"_min"] = min(values[key+"_min"], dp[key])
                    values[key+"_max"] = max(values[key+"_max"], dp[key])
                    
            elif isinstance(dp[key], str):
                try:
                    values[key].append(dp[key])
                except:
                    values[key] = []
    return values
    

# __________R_____A_____N_____D_____O_____M_____I_____Z_____E__________

def randomize(json_file: str, p: float):
    """
    json_file: name of data file as string
    p: probability of each datapoint to be altered ([0, 1])
    """
    # overview of what has been altered
    summary = {"unchanged": 0, "changed": 0, 
               "added": 0, "removed": 0, "skewed": 0}

    os.makedirs("datasets_altered", exist_ok=True)
    modified = json_file[:-len('.json')] + str(int(p*100)) + '.json'

    # new data list
    new_data = []

    # with open(f"datasets_altered\{modified}", 'w') as f:
    with open(json_file, 'r') as original:
        data = json.load(original)
        stats = statistics(data)

        for point in data:
            if random.random() < 1-p:       # copy datapoint
                summary["unchanged"] += 1
                new_data.append(point)
            else:                           # modify point
                summary["changed"] += 1

                action = random.random()
                if action < 1/3:                # - skew
                    summary["skewed"] += 1
                    for key in point.keys():
                        # multiply int and float values with random number between 0.5 and 1.5
                        change = toChange(json_file[:-5]+"_source.json")
                        if type(point[key]) == int and key in change:
                            point[key] = int(point[key]*random.randint(5,15)/10)
                        
                        elif type(point[key]) == float and key in change:
                            point[key] = round(point[key]*random.randint(5,15)/10, 3)
                    new_data.append(point)
                    
                elif action < 2/3:              # - remove
                    summary["removed"] += 1
                    continue

                else:                           # - add
                    summary["added"] += 1
                    modified_point = {}

                    for k in data[0]:
                        if isinstance(point[k], int) and k != "_ID_":
                            modified_point[k] = int(random.uniform(stats[k+"_max"], stats[k+"_min"]))
                        
                        elif isinstance(point[k], float):
                            modified_point[k] = round(random.uniform(stats[k+"_max"], stats[k+"_min"]), 3)

                        elif isinstance(point[k], str):
                            modified_point[k] = random.choice(stats[k])

                    new_data.append(modified_point)

    with open(f"datasets_altered/{modified}", 'w') as f:
        json.dump(new_data, f, indent=2)                    

    proportion = round(100*summary['changed']/(summary['unchanged']+summary['changed']), 2)
    summary["amountOfChange"] = f"{proportion}%"

    return summary


# TEST WITH IDs
# __________________________________________________________________________________________________________________________

id_sets = ["cars", "iris"]

print(toChange("id_datasets/[id]_" + id_sets[0] + "_source.json"))

with open("id_datasets/[id]_" + id_sets[0] + ".json", "r") as f:
    data = json.load(f)
    print(statistics(data))

# __________________________________________________________________________________________________________________________
# # randomize all files from 5% to 20% (in steps of 5)
# if __name__ == "__main__":
#     resume = {"5%": [], "10%": [], "15%": [], "20%": []}
#     for i in range(5, 21, 5):
#         print(f"{i}%:")
#         for file in files: 
#             summary = randomize(file, i/100)
            
#             # keep randomizing if nothing changed or values are too far off
#             pos = summary["amountOfChange"].index('.')
#             aoc = int(summary["amountOfChange"][:pos]) # amount of change as int

#             while summary["changed"] == 0:
#                 print("no change")
#                 summary = randomize(file, i/100)

#             while aoc not in range(i-4, i+4):
#                 print("too far off")
#                 summary = randomize(file, i/100)
#                 pos = summary["amountOfChange"].index('.')
#                 aoc = int(summary["amountOfChange"][:pos])

#             resume[f"{i}%"].append(summary["amountOfChange"])
#             print(f"'{file}' has been altered and saved as '{file[:-5]}{i}.json'.")
#             print(f"Summary of change: {summary}\n")
    
#     print(json.dumps(resume, indent=2))