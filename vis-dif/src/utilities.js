// translation of python compare function to javascript
const props = require('../globals.json');

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
            dp_a._type_ = "removed";
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
            dp_b._type_ = "added";
            diffs.push(dp_b);
        }
    }
    // specs - mandatory
    const mark = JSON.parse(JSON.stringify(a_json.mark));
    const encoding = JSON.parse(JSON.stringify(a_json.encoding));

    // add tooltip
    if (encoding.tooltip) {
        encoding.tooltip.unshift({ "field": "_type_" });
    } else { 
        encoding.tooltip = [{ "field": "_type_" }];
    }

    const output_vl = {
        width: "container",
        height: "container",
        background: null,
        config: {
            legend: {labelColor: '#3a393f', titleColor: "black"},
            axis: { gridColor: "black" },
            axisX: { labelColor: '#3a393f', titleColor: "black" },
            axisY: { labelColor: '#3a393f', titleColor: "black" },
        },
        data: {values: diffs},
        mark: mark,
        encoding: encoding,
        $schema: "https://vega.github.io/schema/vega-lite/v4.17.0.json"
    };

    // specs - optional
    try {
        const selection = a_json.selection;
        output_vl.selection = selection;
    } catch (err) {}
    return output_vl;
    }


// translation of formatSpecs.py as function
export function formatSpecs(file) {
    var data = null;
    try {
        data = file.datasets[file.data.name];
    } catch (err) {
        data = file.data.values;
    }
    const mark = file.mark;
    const encoding = file.encoding;
    const formatted = {
        width: "container",
        height: "container",
        background: null,
        config: {
            legend: {labelColor: '#3a393f', titleColor: "black"},
            axis: { gridColor: "black" },
            axisX: { labelColor: '#3a393f', titleColor: "black" },
            axisY: { labelColor: '#3a393f', titleColor: "black" },
        },
        data: {values: data},
        mark: mark,
        encoding: encoding,
        $schema: "https://vega.github.io/schema/vega-lite/v4.17.0.json"
    };
    return formatted;
}