# import section
import json
import glob
import os
import random

# change path to where json files are
os.chdir("BachelorThesis\datasets")

abs_path = os.getcwd()
json_files = abs_path + "\*.json"

# scan for all .json files in this folder
files = glob.glob(json_files)

for i, file in enumerate(files):
    files[i] = os.path.split(file)[-1]

    
# __________M_____O_____D_____I_____F_____I_____C_____A_____T_____I_____O_____N__________

def modify(point: dict):
    action = random.random()
    for key in point.keys():
        if type(point[key]) == int or type(point[key]) == float:
            # 1. Skew
            if action < 1/2:
                # multiply value with random number between 0.5 and 1.5
                point[key] = point[key]*random.randint(5,15)/10

            # 2. Remove already done in Randomization
            
            # 3. Add
            else:
                pass
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

    with open(f"datasets_altered\{modified}", 'w') as f:
        with open(json_file, 'r') as original:
            data = json.load(original)
            f.write("[\n")
            
            for point in data[:-1]:
                # string = ""
                if random.random() < 1-p:
                    # just copy
                    string = str(point)
                    string = string.replace("'", "\"").replace("None", "null")
                    f.write(f"\t{string},\n")
                else:
                    # modify(point)
                    if random.random() < 1/3:
                        del point
                    else:
                        string = modify(point)
                        string = string.replace("'", "\"").replace("None", "null")
                        f.write(f"\t{string},\n")

            # last item handled seperately because of trailing comma
            if random.random() < 1-p:
                # just copy
                string = str(data[-1])
            else:
                # modify(point)
                string = modify(data[-1])
            string = string.replace("'", "\"").replace("None", "null")
            f.write(f"\t{string}\n")
            f.write("]")
    print(f"'{json_file}' has been altered and saved as '{modified}' in folder 'datasets_altered'.")


# randomize all test files from 1% to 20% (in steps of 1)
if __name__ == "__main__":
    for file in files:
        for i in range(1, 21):
            randomize(file, i/100)