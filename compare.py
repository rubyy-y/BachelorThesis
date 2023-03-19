# import section
import os
import json


os.chdir("BachelorThesis\datasets\sources")


def statistics(a):
    """
    This function takes one JSON file as input
    and returns general statistics for the data
    """
    with open(a, "r") as f:
        source = json.load(f)
        print(source.keys())

        config = source['config']
        data = source['data']
        mark = source['mark']
        encoding = source['encoding']
        schema = source['$schema']
        datasets = source['datasets']

        print(datasets.keys())



def compare(a, b):
    """
    This function takes two JSON files as input
    and outputs general statistics and distinct datapoints that differ
    """
    return a == b


statistics("iris_source.json")
