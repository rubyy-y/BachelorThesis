import './App.css';
import React, { useState } from "react";
import vegaEmbed from 'vega-embed';

function App() {
  const [select, setSelect] = useState("iris");

  const data = {
    anscombe: 'anscombe',
    barley: 'barley',
    burtin: 'burtin',
    cars: 'cars',
    crimea: 'crimea',
    driving: 'driving',
    iris: 'iris',
    ohlc: 'ohlc',
    wheat: 'wheat',
  };

  const handleChange = (e) => {
    setSelect(e.target.options[e.target.selectedIndex].value);
  };

  var original = "data/" + data[select] + "_source.json";
  vegaEmbed('#vis1', original, {"actions": false});

  // TODO - int of variability change by slider
  var altered = "data/" + data[select]+'20_source.json';
  vegaEmbed('#vis2', altered, {"actions": false});

  var comp = "data/comparisons/" + data[select] + "_COMP_" + select + "20.json"; 
  vegaEmbed('#dif', comp, {"actions": false});

  return (
    <div className="App">
      <header className="App-header">
        <p>Highlighting Differences in Data Visualizations</p>
      </header>

      <div className="body">
        <div className="dropdown">
          <label for="datasets">Choose a dataset: </label>
          <select value={select} onChange={handleChange}>
            <option value="anscombe">anscombe.json</option>
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
