# import section
import os
import glob
import json
import random

# change path to where json files are
os.chdir("BachelorThesis\datasets")
json_files = os.getcwd() + "\*.json"

# scan for all .json files in this folder
files = [os.path.split(file)[-1] for file in glob.glob(json_files)]


# _______________________________________
def getNotXYColor(file):
    """
    file: json source file
    This function returns a list of the values that are NOT encoded
    in the x or y field of the vega lite spec.
    """
    with open("../vis-dif/public/data/" + file) as f:
        f_vl = json.load(f)
        keys = list(f_vl["datasets"][list(f_vl["datasets"].keys())[0]][0].keys())
        
        keys.remove(f_vl["encoding"]["x"]["field"])
        keys.remove(f_vl["encoding"]["y"]["field"])
        return keys
    

# __________R_____A_____N_____D_____O_____M_____I_____Z_____E__________

def randomize(json_file: str, p: float):
    """
    json_file: name of data file as string
    p: probability of each datapoint to be altered ([0, 1])
    """
    # overview of what has been altered
    summary = {"unchanged": 0, "changed": 0, 
               "added": 0, "removed": 0, "skewed": 0}

    # generate new directory for altered files
    os.makedirs("datasets_altered", exist_ok=True)

    # open original file in read mode and create [json_file][p].json in write mode
    modified = json_file[:-len('.json')] + str(int(p*100)) + '.json'

    # new data list
    new_data = []

    # with open(f"datasets_altered\{modified}", 'w') as f:
    with open(json_file, 'r') as original:
        data = json.load(original)
        
        for point in data:
            # just copy
            if random.random() < 1-p:
                summary["unchanged"] += 1
                new_data.append(point)
            else:
                # modify point
                action = random.random()
                
                # 1. SKEW
                if action < 1/3:
                    summary["changed"] += 1
                    summary["skewed"] += 1
                    for key in point.keys():
                        # multiply value with random number between 0.5 and 1.5
                        unchanged = getNotXYColor(json_file[:-5]+"_source.json")
                        if type(point[key]) == int and key not in unchanged:
                            point[key] = int(point[key]*random.randint(5,15)/10)
                        
                        elif type(point[key]) == float:
                            point[key] = round(point[key]*random.randint(5,15)/10, 3)

                    new_data.append(point)
                    
                # 2. REMOVE
                elif action < 2/3:
                    summary["changed"] += 1
                    summary["removed"] += 1
                    continue

                # 3. ADD
                else: 
                    summary["changed"] += 1
                    summary["added"] += 1

                    stats = {}
                    for key in data[0].keys():
                        values = [dp[key] for dp in data if isinstance(dp[key], (int, float)) and dp[key] is not None]
                        if values:
                            stats[key + "_min"] = min(values)
                            stats[key + "_max"] = max(values)

                        elif isinstance(data[0][key], str):
                            stats[key] = list({dp[key] for dp in data if dp[key] is not None})

                    modified_point = {}
                    for k in data[0].keys():
                        value_type = type(data[0][k])

                        if value_type == int:
                            modified_point[k] = int(random.uniform(stats[k+"_max"], stats[k+"_min"]))
                        
                        elif value_type == float:
                            modified_point[k] = random.uniform(stats[k+"_max"], stats[k+"_min"])

                        elif value_type == str:
                            modified_point[k] = random.choice(stats[k])

                    new_data.append(modified_point)

    with open(f"datasets_altered/{modified}", 'w') as f:
        json.dump(new_data, f, indent=2)                    
    
    try:
        proportion = round(100*summary['changed']/summary['unchanged'], 2)
        summary["amountOfChange"] = f"{proportion}%"
    except:
        summary["amountOfChange"] = "failed"
    return summary

# print(getNotXYColor("burtin_source.json"))
# randomize("burtin.json", 0.7)

# randomize all files from 5% to 20% (in steps of 5)
if __name__ == "__main__":
    resume = {"5%": [], "10%": [], "15%": [], "20%": []}
    for i in range(5, 21, 5):
        print(f"{i}%:")
        for file in files: 
            summary = randomize(file, i/100)
            resume[f"{i}%"].append(summary["amountOfChange"])
            print(f"'{file}' has been altered and saved as '{file[:-5]}{i}.json'.")
            print(f"Summary of change: {summary}\n")
    
    print(json.dumps(resume, indent=2))