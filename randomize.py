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

# __________M_____O_____D_____I_____F_____I_____C_____A_____T_____I_____O_____N__________

def modify(point: dict, file: str):
    action = random.random()
    
    # 1. SKEW
    if action < 1/2:
        for key in point.keys():
            # multiply value with random number between 0.5 and 1.5
            unchanged = getNotXYColor(file[:-5]+"_source.json")
            if type(point[key]) == int and key not in unchanged:
                point[key] = int(point[key]*random.randint(5,15)/10)
            
            elif type(point[key]) == float:
                point[key] = round(point[key]*random.randint(5,15)/10, 3)

    # 3. ADD
    else:        
        stats = {}
        with open(file, "r") as f:
            source = json.load(f)
            for key in source[0].keys():
                # if type(source[0][key]) == int or type(source[0][key]) == float:
                #     # try:
                #     minimum = min([dp[key] for dp in source if dp[key]!=None])
                #     maximum = max([dp[key] for dp in source if dp[key]!=None])
                    
                #     stats[key+"_min"] = minimum
                #     stats[key+"_max"] = maximum

                #     # except TypeError:
                #     #     pass

                # elif type(source[0][key]) == str:
                #     stats[key] = list({dp[key] for dp in source})

                values = [dp[key] for dp in source if isinstance(dp[key], (int, float)) and dp[key] is not None]
                if values:
                    stats[key + "_min"] = min(values)
                    stats[key + "_max"] = max(values)

                elif isinstance(source[0][key], str):
                    stats[key] = list({dp[key] for dp in source if dp[key] is not None})

        point = {}
        for k in source[0].keys():
            value_type = type(source[0][k])

            if value_type == int:
                point[k] = int(random.uniform(stats[k+"_max"], stats[k+"_min"]))

            elif value_type == float:
                point[k] = random.uniform(stats[k+"_max"], stats[k+"_min"])

            elif value_type == str:
                point[k] = random.choice(stats[k])

    return str(point).replace("'", "\"").replace("None", "null")


# __________R_____A_____N_____D_____O_____M_____I_____Z_____E__________

def randomize(json_file: str, p: float):
    """
    json_file: name of data file as string
    p: probability of each datapoint to be altered
    """
    # Error Handling
    if p < 0.01 or p > 1:
        raise ValueError("Please choose p in range [0.01, 1]")

    # generate new directory for altered files
    os.makedirs("datasets_altered", exist_ok=True)

    # open original file in read mode and create [json_file][p].json in write mode
    modified = json_file[:-len('.json')] + str(int(p*100)) + '.json'

    with open(f"datasets_altered\{modified}", 'wb') as f:
        with open(json_file, 'r') as original:
            data = json.load(original)
            f.write(bytes("[\n", 'utf-8'))
            
            for point in data:
                if random.random() < 1-p:
                    # just copy
                    string = str(point)
                    string = string.replace("'", "\"").replace("None", "null")
                    f.write(bytes(f"\t{string},\n", 'utf-8'))
                else:
                    # modify point
                    if random.random() < 1/3:
                        # because modified is the only one opened in write-mode
                        # 2. REMOVE
                        del point
                    else:
                        string = modify(point, json_file)
                        string = string.replace("'", "\"").replace("None", "null")
                        f.write(bytes(f"\t{string},\n", 'utf-8'))
            
            # delete last comma
            f.seek(-2, 2)
            f.truncate()

            f.write(bytes("\n]", 'utf-8'))
    return None

print(getNotXYColor("burtin_source.json"))
randomize("burtin.json", 0.7)

# # randomize all files from 5% to 20% (in steps of 5)
# if __name__ == "__main__":
#     for file in files:
#         for i in range(5, 21, 5):
#             randomize(file, i/100)
#             print(f"'{file}' has been altered and saved as '{file[:-5]}{i}.json'.")
