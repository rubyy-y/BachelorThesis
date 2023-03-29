import './App.css';

function App() {
  return (
    <div className="App">
      
      <header className="App-header">
        <p>
          Highlighting Differences in Data Visualizations
        </p>
      </header>

      <body>
        <div className="dropdown">
          <label for="datasets">Choose a dataset: </label>
          <select name="dog-names" id="dog-names">
            <option value="iris">anscombe.json</option>
            <option value="cars">barley.json</option>
            <option value="wheat">burtin.json</option>
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
      </body>
    </div>
  );
}

export default App;
