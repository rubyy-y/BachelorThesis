# Highlighting Differences in Data Visualizations
> "This project aims to **identify and annotate differences** between two **data visualizations** created using the **Vega-Lite grammar**. Vega-Lite uses a **JSON syntax** to define mappings from data to **properties of graphical marks**. Given two Vega-Lite specifications, the project will **compare the JSON** and resulting visualizations and **highlight any differences** by annotating them within the visualization itself, making it easy to spot and understand the changes. [...]"

**Research Question: How can updates to data or specifications of visualizations be explained?**

Implementation: Web Application using **React, JavaScript, Python, HTML** and **CSS**.

The (Altair) Visualization offers an option called "View Source". This source code will later serve to compare two visualizations! <br>
**note to self:** Make file where you document exploration of JSON files, or special characteristics to later include in thesis.


## Project Must-Haves
<ul>
    <li> Data randomization Function </li>
    <ul>
        <li> Input: JSON file, probability of change </li>
        <li> Output: same JSON, some datapoints different (added, removed, skewed, recolored) </li>
        <li> is saved as [dataset name][probability of change].json </li>
        <ul> 
            <li> example: cars30.json is car dataset where every datapoint has 35% probability of being altered (with Modification Function). </li> 
        </ul>
    </ul>
    <li> Datapoint Modification Function </li>
    <ul>
        <li> Input: JSON datapoint </li>
        <li> Output: </li>
        <li> with probability of 1/3: </li>
        <ul>
            <li> add: same datapoint and a second, random datapoint </li>
            <li> remove: None </li>
            <li> skew: datapoint with similar values (maybe based on density of all datapoints) </li>
        </ul>
    </ul>
    <li> JSON Comparison Function </li>
    <ul>
        <li> Input: two compiled Vega JSON files </li>
        <li> Output: </li>
        <ul>
            <li> general statistics: how many datapoints in each dataset, amount of difference (in %) </li>
            <li> datapoints missing </li>
            <li> datapoints added </li>
            <li> datapoints differently colored (= Label changed) </li>
        </ul>
    </ul>
    <li> Usable Web Application </li>
    <ul>
        <li> Showing Dataset </li>
        <li> Showing randomized Version of Dataset </li>
        <li> Third Visualization of clear differences </li>
    </ul>
</ul>

## Project Nice-To-Haves
<ul>
    <li> User decides what Dataset </li>
    <li> User decides Randomization </li>
    <li> User decides if color counts as difference -> Boolean Value in input </li>
    <li> In comparison function: 
    <ul> 
        <li> Recognize datapoints that might have been shifted, </li>
        <li> based on some Threshold (hyperparameter) of distance between a deleted and an added datapoint. </li>
    </ul>
</ul>