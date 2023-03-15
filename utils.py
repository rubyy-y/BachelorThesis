# import section
import json
import glob
import os
import random

# absolute path to where json files are
abs_path = fr"C:\Users\rubin\OneDrive\Desktop\University\BachelorThesis\datasets_test"
json_files = abs_path + "\*.json"

# scan for all .json files in this folder
files = glob.glob(json_files)

for i, file in enumerate(files):
    files[i] = os.path.split(file)[-1]

# only accept non-altered files
for file in files:
    if file.endswith('percent.json'):
        files.remove(file)

# change current working directory to this directory
os.chdir(abs_path)
    
# __________M_____O_____D_____I_____F_____I_____C_____A_____T_____I_____O_____N__________

def modify(point):
    # 1. Skew
    if random.random() < 1/3:
        amount = random.randint(5,8)/10
        return(amount*point)

    # 2. Remove
    elif random.random() < 2/3:
        pass
    

    # 3. Add
    else:
        pass

# _____J__S__O__N_______S__T__R_____
def json_str(string: str):
    """
    This method transforms a string into JSON syntax;
    ' becomes "
    None becomes null
    """
    string = string.replace("'", "\"")
    string = string.replace("None", "null")
    return string

# __________R_____A_____N_____D_____O_____M_____I_____Z_____E__________

def randomize(json_file: str, p: float):
    """
    json_file: name of file as string
    p: probability of each datapoint to be altered
    """
    # Error Handling
    if p < 0.01 or p > 1:
        raise ValueError("Please choose p in range [0.01; 1]")


    #### PROBLEM: the trailing comma in the last datapoint needs fo be removed #####

    # open original file in read mode and create [json_file][p]percent.json in write
    modified = json_file[:-len('.json')] + str(int(p*100)) + 'percent.json'

    with open(modified, 'w') as f:
        with open(json_file, 'r') as original:
            data = json.load(original)
            f.write("[\n")
            for i, point in enumerate(data):

                # while it is not the last datapoint in the set
                if i != len(data)-1:

                    if random.random() < 1-p:
                        string = json_str(str(point))
                        f.write(f"\t{string},\n")

                    else:
                        for key in point.keys():
                            if type(point[key]) == int or type(point[key]) == float:
                                point[key] = modify(point[key])
                        
                        string = json_str(str(point))
                        f.write(f"\t{string},\n")
                
                # last datapoint is never altered to ensure JSON syntax is not disrupted by leading comma
                else:
                    string = json_str(str(point))
                    f.write(f"\t{string}\n")
            f.write("]")

    print(f"'{json_file}' has been altered and saved as '{modified}'")


# randomize all test files from 5% to 20% (in steps of 5)
for file in files:
    for i in range(5, 21, 5):
        print(file)
        randomize(file, i/100)



# __________I_____G_____N_____O_____R_____E__________
# randomize('cars_test.json', 0.6)

# # probability check
# tries = 100000
# count = 0
# for i in range(tries):
#     if random.random() < 0.2:
#         count += 1

# print(f"Percentage = {count/tries}%")