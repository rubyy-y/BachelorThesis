# Highlighting Differences in Data Visualizations
> "This project aims to **identify and annotate differences** between two **data visualizations** created using the **Vega-Lite grammar**. Vega-Lite uses a **JSON syntax** to define mappings from data to **properties of graphical marks**. Given two Vega-Lite specifications, the project will **compare the JSON** and resulting visualizations and **highlight any differences** by annotating them within the visualization itself, making it easy to spot and understand the changes. [...]"

Implementation: Web Application using **JSON**, **JavaScript, Python, HTML** and **CSS**.

### Current Plan

Web Application shows two divisions: 
<ol> 
    <li> Original dataset from vega-datasets and</li>
    <li> randomized version of the same dataset. </li>
</ol> 

The (Altair) Visualization offers an option called "View Compiled Vega". This source code will later serve to compare two visualizations! <br>
**TODO:** Make file where you document differences in JSON files, or special characteristics to later include in Report.


## Project Must-Haves
<ul>
    <li> Usable Web Application </li>
    <li> Showing Dataset (not necessarily from JSON)</li>
    <li> Showing randomized Version of Dataset </li>
    <li> Third Visualization of clear differences </li>
</ul>

## Project Nice-To-Haves
<ul>
    <li> User decides what Dataset </li>
    <li> User decides Ranomization </li>
    <li> User decides what counts as "difference" (color, position) </li>
</ul>