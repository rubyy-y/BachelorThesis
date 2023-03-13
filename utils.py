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
# !!!! ERROR - ALSO LISTS ALREADY MODIFIED FILES !!!!
files = glob.glob(json_files)
for i, file in enumerate(files):
    files[i] = os.path.split(file)[-1]

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


# __________R_____A_____N_____D_____O_____M_____I_____Z_____E__________

def randomize(json_file: str, p: float):
    """
    json_file: name of file as string
    p: probability of each datapoint to be altered
    """
    # Error Handling
    if p < 0.01 or p > 1:
        raise ValueError("Please choose p in range [0.01; 1]")

    ### ONLY WORKS FOR IRIS DATASET BECAUSE OF JSON STRUCTURE ###
    #### also, in the copied version, the trailing comma in ####
    ##### the last datapoint needs fo be removed manually #####

    # open original file in read mode and create [json_file][p].json in write
    modified = json_file[:-len('.json')] + str(int(p*100)) + '.json'

    with open(modified, 'w') as f:
        with open(json_file, 'r') as original:
            data = json.load(original)
            f.write("[\n")
            for point in data:
                if random.random() < 1-p:
                    # replace ' with " for json file
                    string = str(point).replace("'", "\"")
                    f.write(f"  {string},\n")

                else:
                    for key in point.keys():
                        if type(point[key]) == int or type(point[key]) == float:
                            point[key] = modify(point[key])
                            # replace ' with " for json file
                    string = str(point).replace("'", "\"")
                    f.write(f"  {string},\n")
            f.write("]")
        

    """ ### THIS DID NOT WORK YET BECAUSE OF WRITING TO FILE PROBLEMS; BETTER OPTION HOWEVER!!
    # make copy of file and save as [json_file][p].json
    copy = json_file[:-len('.json')] + str(int(p*100)) + '.json'
    
    # this might only work on windows, easily extendable for other machines
    # if not path.isfile(copy):
    if save:
        os.system(f'copy {json_file} {copy}')

    # wrong mode
    with open(copy, 'r+') as f:
        data = json.load(f)
        print(type(data))

        for i, point in enumerate(data):
            if random.random() < p:
                keys = list(point.keys())

                # check datatype of key, if int or float: change
                for key in keys:
                    # print(key)
                    if type(point[key]) == int or type(point[key]) == float:
                        # print("Before:", point[key])
                        
                        # point[key] = modify(point[key])
                        
                        print("Before:", data[i][key])
                        data[i][key] = modify(point[key])
                        print("After:", data[i][key])

                        # print("After:", point[key])
    """


randomize(files[0], 0.6)

# __________I_____G_____N_____O_____R_____E__________
# # probability check
# tries = 100000
# count = 0
# for i in range(tries):
#     if random.random() < 0.2:
#         count += 1

# print(f"Percentage = {count/tries}%")