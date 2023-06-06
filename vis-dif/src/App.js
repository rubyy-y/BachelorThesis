import './App.css';
import React, { useState, useEffect } from "react";
import vegaEmbed from 'vega-embed';

import { compare, formatSpecs } from './utilities.js';

function App() {
  const [select, setSelect] = useState("iris");
  const [percent, setPercent] = useState("20");
  const [file1Content, setFile1Content] = useState(null);
  const [file2Content, setFile2Content] = useState(null);
  const theme = 'quartz';

  useEffect(() => {
    // File 1 was uploaded
    if (file1Content) {
      const file1Formatted = formatSpecs(file1Content);
      vegaEmbed('#vis1', file1Formatted, {"actions": false, "theme": theme});
      
      // File 2 was uploaded
      if (file2Content) {
        const file2Formatted = formatSpecs(file2Content);
        vegaEmbed('#vis2', file2Formatted, {"actions": false, "theme": theme});

        const spec = compare(file1Content, file2Content);
        // No difference
        if (spec.data.values.length === 0) {
          document.getElementById("dif").innerHTML = "The two visualizations are visually identical.";
        // Difference
        } else {
          vegaEmbed('#dif', spec, {"actions": false, "theme": theme});
        }
      
      // File 2 was not uploaded
      } else {
        document.getElementById("vis2").innerHTML = "Upload second file.";
        document.getElementById("dif").innerHTML = "Visualization will appear once a second file was uploaded.";
      } 
    } else {
      var original = "data/" + select + "_source.json";
      var altered = "data/" + select + percent + '_source.json';
      var comp = "data/comparisons/" + select + "_COMP_" + select + percent + ".json";
      vegaEmbed('#vis1', original, {"actions": false, "theme": theme});
      vegaEmbed('#vis2', altered, {"actions": false, "theme": theme});
      vegaEmbed('#dif', comp, {"actions": false, "theme": theme});
    }
  }, [select, percent, file1Content, file2Content]);  

  const handleChange = (e) => {
    setSelect(e.target.options[e.target.selectedIndex].value);
    setFile1Content(null);
    setFile2Content(null);
    console.log(file1Content, file2Content);
  };

  const handleFileUpload1 = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = JSON.parse(event.target.result);
      setFile1Content(content);
    };
    reader.onabort = () => {
      setFile1Content(null);
    };
    reader.readAsText(file);
  }; 

  const handleFileUpload2 = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = JSON.parse(event.target.result);
      setFile2Content(content);
    };
    reader.onabort = () => {
      setFile2Content(null);
    };
    reader.readAsText(file);
  };   

  return (
    <div className="App">
      <header className="App-header">
        <p>Highlighting Differences in Data Visualizations</p>
      </header>
  
      <div className="body">
        <div className="dropdown">
          <label htmlFor="datasets">Choose a dataset: </label>
          <select value={select} onChange={handleChange}>
            <option value="barley">barley.json</option>
            <option value="burtin">burtin.json</option>
            <option value="cars">cars.json</option>
            <option value="crimea">crimea.json</option>
            <option value="driving">driving.json</option>
            <option value="iris">iris.json</option>
            <option value="ohlc">ohlc.json</option>
            <option value="wheat">wheat.json</option>
          </select>
        </div>
  
        <div className="radio">
          <label htmlFor="per">Select a degree of variation: <br/></label>
          <input type="radio" name="percent" value="5" checked={percent === "5"} onChange={(e) => setPercent(e.target.value)}/>5%
          <input type="radio" name="percent" value="10" checked={percent === "10"} onChange={(e) => setPercent(e.target.value)}/>10%
          <input type="radio" name="percent" value="15" checked={percent === "15"} onChange={(e) => setPercent(e.target.value)}/>15%
          <input type="radio" name="percent" value="20" checked={percent === "20"} onChange={(e) => setPercent(e.target.value)}/>20%
        </div>
  
        <div id="vis1" className="vis1">
          This is where the first Visualization will go.
        </div>
  
        <div id="vis2" className="vis2">
          This is where the second Visualization will go.
        </div>
  
        <p>or choose your own JSON files:</p>
  
        <div className="file1">
          <input type="file" id="fileUpload1" accept=".JSON" onChange={handleFileUpload1}></input>
        </div>
        <div className="file2">
          <input type="file" id="fileUpload2" accept=".JSON" onChange={handleFileUpload2}></input>
        </div>
  
        <div id="dif" className="dif">
          This is where a visualization of the differences will appear.
        </div>
      </div>
    </div>
  );  
}

export default App;
