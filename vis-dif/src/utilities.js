// translation of python compare function to javascript

export function compare(a_json, b_json) {
// x and y values
const a_x = a_json.encoding.x.field;
const a_y = a_json.encoding.y.field;
const b_x = b_json.encoding.x.field;
const b_y = b_json.encoding.y.field;

// datapoints
var data_a = null;
try {
    data_a = a_json.datasets[a_json.data.name];
} catch (err) {
    data_a = a_json.data.values;
}

var data_b = null;
try {
    data_b = b_json.datasets[b_json.data.name];
} catch (err) {
    data_b = b_json.data.values;
}

console.log(data_a, data_b);

// save differences to list of dictionaries
const diffs = [];

// iterate through first file
for (const dp_a of data_a) {
    let identical = false;
    for (const dp_b of data_b) {
    if (dp_a[a_x] === dp_b[b_x] && dp_a[a_y] === dp_b[b_y]) {
        identical = true;
        break;
    }
    }
    if (!identical) {
    diffs.push(dp_a);
    }
}

// iterate through second file
for (const dp_b of data_b) {
    let identical = false;
    for (const dp_a of data_a) {
    if (dp_a[a_x] === dp_b[b_x] && dp_a[a_y] === dp_b[b_y]) {
        identical = true;
        break;
    }
    }
    if (!identical) {
    diffs.push(dp_b);
    }
}

// specs - mandatory
var hash_ = null;
try {
    hash_ = a_json.data.name;
} catch (err) {
    // hash_ = a_json.data.values;
}
const mark = a_json.mark;
const encoding = a_json.encoding;
// encoding.color.legend = null;

const output_vl = {
    width: "container",
    height: "container",
    background: null,
    config: {
    axis: { gridColor: "white" },
    axisX: { labelColor: "white", titleColor: "white" },
    axisY: { labelColor: "white", titleColor: "white" },
    },
    data: { name: hash_ },
    mark: mark,
    encoding: encoding,
    $schema: "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    datasets: { [hash_]: diffs },
};

// specs - optional
try {
    const selection = a_json.selection;
    output_vl.selection = selection;
} catch (err) {}

// output_vl.encoding.color.legend = null;
console.log(output_vl);
return output_vl;
}


// translation of formatSpecs.py as function

export function formatSpecs(file) {
    const props = {
        "width": "container",
        "height": "container",
        "background": null,
        "config": {
            "legend": {"labelColor": "white", "titleColor": "white"},
            "axis": {"gridColor": "white"},
            "axisX": {"labelColor": "white", "titleColor": "white"},
            "axisY": {"labelColor": "white", "titleColor": "white"}
                }
    }

    // console.log(file.data.values);
    return file;
}