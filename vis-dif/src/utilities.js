// translation of python compare function to javascript

export function compare(a_json, b_json) {
    const config = require("./globals.json");
    const props = config.VL;

    // x and y values
    const a_x = a_json.encoding.x.field;
    const a_y = a_json.encoding.y.field;
    const b_x = b_json.encoding.x.field;
    const b_y = b_json.encoding.y.field;
    const color = a_json.encoding.color.field;

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

    // save differences to list
    const diffs = [];

    if (a_json.mark === "bar") { // Barplot
        for (let dp_a of data_a) {
            let identical = false;
            for (let dp_b of data_b) {
                if ([a_x, color].every(key => dp_a[key] === dp_b[key])) {
                    identical = true;
        
                    // altered?
                    let dif = JSON.parse(JSON.stringify(dp_a));

                    let difference = dp_a[a_y] - dp_b[b_y];
                    dif[a_y] = difference * -1;
        
                    if (difference < 0) {
                        dif["_type_"] = "altered; added";
                    } else if (difference > 0) {
                        dif["_type_"] = "altered; removed";
                    }

                    diffs.push(dif);
                    break;
                }
            }
            if (!identical) {
                let rem = JSON.parse(JSON.stringify(dp_a));
                rem["_type_"] = "completely removed";
                rem[a_y] *= -1;
                diffs.push(rem);
            }
        }
        
        for (let dp_b of data_b) {
            let identical = false;
            for (let dp_a of data_a) {
                if ([a_x, color].every(key => dp_a[key] === dp_b[key])) {
                    identical = true;
                    break;
                }
            }
            if (!identical) {
                let add = JSON.parse(JSON.stringify(dp_b));
                add["_type_"] = "completely added";
                diffs.push(add);
            }
        };

    } else { // Scatterplot
        // iterate through first file
        for (const dp_a of data_a) {
            let identical = false;
            for (const dp_b of data_b) {
                if (dp_a[a_x] === dp_b[b_x] && dp_a[a_y] === dp_b[b_y]) {
                    identical = true;
                    break;
                };
            };
            if (!identical) {
                dp_a._type_ = "removed";
                diffs.push(dp_a);
            };
        };
        // iterate through second file
        for (const dp_b of data_b) {
            let identical = false;
            for (const dp_a of data_a) {
                if (dp_a[a_x] === dp_b[b_x] && dp_a[a_y] === dp_b[b_y]) {
                    identical = true;
                    break;
                };
            };
            if (!identical) {
                dp_b._type_ = "added";
                diffs.push(dp_b);
            };
        };
    }
   
    // Make new specifiation
    const mark = JSON.parse(JSON.stringify(a_json.mark));
    const encoding = JSON.parse(JSON.stringify(a_json.encoding));

    if (encoding.tooltip) {
        encoding.tooltip.unshift({ "field": "_type_" });
    } else { 
        encoding.tooltip = [{ "field": "_type_" }];
    }

    const spec = JSON.parse(JSON.stringify(props));
    spec.data = {values: diffs};
    spec.mark = mark;
    spec.encoding = encoding;
    spec.$schema = "https://vega.github.io/schema/vega-lite/v4.17.0.json";

    return spec;
    }


// translation of formatSpecs.py as function
export function formatSpecs(file) {
    const config = require("./globals.json");
    const props = config.VL;

    var data = null;
    try {
        data = file.datasets[file.data.name];
    } catch (err) {
        data = file.data.values;
    }
    const mark = file.mark;
    const encoding = file.encoding;

    const spec = JSON.parse(JSON.stringify(props));
    spec.data = {values: data};
    spec.mark = mark;
    spec.encoding = encoding;
    spec.$schema = "https://vega.github.io/schema/vega-lite/v4.17.0.json";

    return spec;
}