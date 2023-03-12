# import section
import json
import glob
import os
import random
from os import path

# absolute path to where json files are
abs_path = fr"C:\Users\rubin\OneDrive\Desktop\University\BachelorThesis\datasets_test"
json_files = abs_path + "\*.json"

# scan for all .json files in this folder
files = glob.glob(json_files)
for i, file in enumerate(files):
    files[i] = os.path.split(file)[-1]

# change current working directory to this directory
os.chdir(abs_path)
    
# __________M_____O_____D_____I_____F_____I_____C_____A_____T_____I_____O_____N__________

def modify():
    pass


# __________R_____A_____N_____D_____O_____M_____I_____Z_____E__________

def randomize(json_file: str, p: float, save: bool):
    """
    json_file: name of file as string
    p: probability of each datapoint to be altered
    """
    # Error Handling
    if p < 0.01 or p > 1:
        raise ValueError("Please choose p in range [0.01; 1]")


    # make copy of file and save as [json_file][p].json
    copy = json_file[:-len('.json')] + str(int(p*100)) + '.json'
    
    # this might only work on windows, easily extendable for other machines
    # if not path.isfile(copy):
    if save:
        os.system(f'copy {json_file} {copy}')

    with open(copy, 'r') as f:
        data = json.load(f)

        for point in data:
            if random.random() < p:
                keys = list(point.keys())

                # check datatype of key, if int or float: change
                for key in keys:
                    if type(point[key]) == int or type(point[key]) == float:
                        print(type(point[key]))

                        # TODO - change

randomize(files[0], 0.01, False)

# __________I_____G_____N_____O_____R_____E__________
# # probability check
# tries = 100000
# count = 0
# for i in range(tries):
#     if random.random() < 0.2:
#         count += 1

# print(f"Percentage = {count/tries}%")