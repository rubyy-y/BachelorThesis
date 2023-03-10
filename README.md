# Highlighting Differences in Data Visualizations
> "This project aims to **identify and annotate differences** between two **data visualizations** created using the **Vega-Lite grammar**. Vega-Lite uses a **JSON syntax** to define mappings from data to **properties of graphical marks**. Given two Vega-Lite specifications, the project will **compare the JSON** and resulting visualizations and **highlight any differences** by annotating them within the visualization itself, making it easy to spot and understand the changes. [...]"

Implementation: Web Application using **JSON**, **JavaScript, Python, HTML** and **CSS**.

# Current Plan

Web Application shows two divisions: 
<ol> 
    <li> Original dataset from vega-datasets and</li>
    <li> randomized version of the same dataset. </li>
</ol> 

**(Idea)** Let user decide on amount of randomization of dataset.

The (Altair) Visualization offers an option called "View Compiled Vega". This source code will later serve to compare two visualizations!

> **TODO**: Look at how to compare the two JSON files

**(Idea)** Let user decide whether color of datapoint should result in highlighted difference, too.
