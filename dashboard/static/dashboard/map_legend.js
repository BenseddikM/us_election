// Info on top right corner:
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// Method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>US Election Results</h4>'
    +  (props ?
        '<b>' + props.name + '</b><br />'
        + props.nb_votes + ' votes <br />'
        + props.max_voters+' eligible voters. <br />'
        + "Winner: "+props.vote_result +"<br />"
        + "Result time: "+props.vote_timestamp +"<br />"

        : 'Hover over a state');
};

info.addTo(map);

// Legend

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 3, 5, 10, 15, 20, 25, 30],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i]) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);

var legendResult = L.control({position: 'bottomright'});

legendResult.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        labels = ["Unknown", "Trump", "Clinton"];

    for (var i = 0; i < labels.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorResult(labels[i]) + '"></i> ' +
            labels[i] +  '<br>';
    }

    return div;
};

legendResult.addTo(map);
