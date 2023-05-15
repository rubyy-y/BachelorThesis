import './App.css';
import React, { useState, useEffect } from "react";
import vegaEmbed from 'vega-embed';

function App() {
  const [select, setSelect] = useState("iris");
  const [percent, setPercent] = useState("20");

  useEffect(() => {
    var original = "data/" + select + "_source.json";
    vegaEmbed('#vis1', original, {"actions": false});

    var altered = "data/" + select+ percent + '_source.json';
    vegaEmbed('#vis2', altered, {"actions": false});

    var comp = "data/comparisons/" + select + "_COMP_" + select + percent + ".json"; 
    vegaEmbed('#dif', comp, {"actions": false});
  }, [select, percent]);

  const handleChange = (e) => {
    setSelect(e.target.options[e.target.selectedIndex].value);
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
          <label>
            <input type="radio" name="percent" value="5" checked={percent === "5"} onChange={(e) => setPercent(e.target.value)}/>
            5%
          </label>
          <label>
            <input type="radio" name="percent" value="10" checked={percent === "10"} onChange={(e) => setPercent(e.target.value)}/>
            10%
          </label>
          <label>
            <input type="radio" name="percent" value="15" checked={percent === "15"} onChange={(e) => setPercent(e.target.value)}/>
            15%
          </label>
          <label>
            <input type="radio" name="percent" value="20" checked={percent === "20"} onChange={(e) => setPercent(e.target.value)}/>
            20%
          </label>
        </div>
  
        <div id="vis1" className="vis1">
          This is where the first Visualization will go.
        </div>
  
        <div id="vis2" className="vis2">
          This is where the second Visualization will go.
        </div>
  
        <p>or choose you own JSON files:</p>
  
        <div className="file2">
          <input type="file" id="fileUpload" accept=".JSON"></input>
        </div>
  
        <div className="file1">
          <input type="file" id="fileUpload" accept=".JSON"></input>
        </div>
  
        <div id="dif" className="dif">
          This is where a visualization of the differences will appear.
        </div>
      </div>
    </div>
  );
  
}

export default App;
