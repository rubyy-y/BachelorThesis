# import section
import os
import glob
import json
import random

# change path to where json files are
os.chdir("BachelorThesis\datasets")
# os.chdir("..")
# os.chdir("../../datasets")

abs_path = os.getcwd()
json_files = abs_path + "\*.json"

# scan for all .json files in this folder
files = [os.path.split(file)[-1] for file in glob.glob(json_files)]

unchanged = ["year", "Cylinders"]

# __________M_____O_____D_____I_____F_____I_____C_____A_____T_____I_____O_____N__________

def modify(point: dict, file: str):
    action = random.random()
    
    # 1. SKEW
    if action < 1/2:
        for key in point.keys():
            # multiply value with random number between 0.5 and 1.5
            if type(point[key]) == int and key not in unchanged:
                point[key] = int(point[key]*random.randint(5,15)/10)
            
            elif type(point[key]) == float:
                point[key] = round(point[key]*random.randint(5,15)/10, 3)

    # 3. ADD
    else:        
        stats = dict()
        with open(file, "r") as f:
            source = json.load(f)
            for key in source[0].keys():
                if type(source[0][key]) == int or type(source[0][key]) == float:
                    try:
                        minimum = min([dp[key] for dp in source if dp[key]!=None])
                        maximum = max([dp[key] for dp in source if dp[key]!=None])
                        
                        stats[key+"_min"] = minimum
                        stats[key+"_max"] = maximum

                    except TypeError:
                        pass

                elif type(source[0][key]) == str:
                    stats[key] = list({dp[key] for dp in source})

        point = dict()
        for k in source[0].keys():
            # values are type int
            if type(source[0][k]) == int:
                point[k] = int(random.uniform(stats[k+"_max"], stats[k+"_min"]))

            # values are type float
            elif type(source[0][k]) == float:
                point[k] = random.uniform(stats[k+"_max"], stats[k+"_min"])

            # values are type string
            elif type(source[0][k]) == str:
                point[k] = random.choice(stats[k])
    return str(point).replace("'", "\"").replace("None", "null")


# __________R_____A_____N_____D_____O_____M_____I_____Z_____E__________

def randomize(json_file: str, p: float):
    """
    json_file: name of file as string
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

    print(f"'{json_file}' has been altered and saved as '{modified}' in folder 'datasets_altered'.")


# randomize all files from 5% to 20% (in steps of 5)
if __name__ == "__main__":
    for file in files:
        for i in range(5, 21, 5):
            randomize(file, i/100)
