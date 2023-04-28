import './App.css';
import React, { useState } from "react";
import vegaEmbed from 'vega-embed';

function App() {
  const [select, setSelect] = useState();

  const data = {
    anscombe: 'data/anscombe_source.json',
    barley: 'data/barley_source.json',
    burtin: 'data/burtin_source.json',
    cars: 'data/cars_source.json',
    crimea: 'data/crimea_source.json',
    driving: 'data/driving_source.json',
    iris: 'data/iris_source.json',
    ohlc: 'data/ohlc_source.json',
    wheat: 'data/wheat_source.json',
  };

  const handleChange = (e) => {
    setSelect(e.target.options[e.target.selectedIndex].value);
  };

  vegaEmbed('#vis1', data[select]);
  vegaEmbed('#vis2', 'data/iris20_source.json');
  vegaEmbed('#dif', 'data/iris_COMP_iris20.json');

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
          <p>You selected {select}</p>
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
