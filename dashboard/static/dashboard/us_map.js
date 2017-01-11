
//Create Base Layer, loads tiles from mapbox
var baseMap = new L.TileLayer('https://api.mapbox.com/styles/v1/leonardbinet/ciw0kj8c500b82klkfevbaje3/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibGVvbmFyZGJpbmV0IiwiYSI6ImNpdzBrNjU4NzAwMmwyb3BrYjQxemRoNnMifQ.7yzHGWbiQtCabkcgHa4oWw'
);

// Create the map
var map = new L.map('map', {
    center: new L.LatLng(37.8, -96),
    zoom: 4,
    maxZoom: 18,
    layers: baseMap
});

// style
var demIcon = L.icon({
    iconUrl: demlogo,
    iconSize:     [38, 95], // size of the icon
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});



// Disable zoom : we use double click to refresh data
map.doubleClickZoom.disable();

function mapInitial(data) {
        map.layer = L.geoJson(data, {
    style: style,
    pointToLayer: function(feature, latlng) {
                return L.marker(latlng, {icon: demIcon});}
                ,
    onEachFeature: onEachFeature
    });
        map.layer.addTo(map);
    }

function mapRefresh(data) {
    map.layer.clearLayers();
    map.layer.addData(data);
}


// Color and style
function getColor(d) {
    return d > 30 ? '#800026' :
           d > 25  ? '#BD0026' :
           d > 20  ? '#E31A1C' :
           d > 15  ? '#FC4E2A' :
           d > 10   ? '#FD8D3C' :
           d > 5   ? '#FEB24C' :
           d > 3   ? '#FED976' :
                      '#FFEDA0';
}
function style(feature) {
    return {
        fillColor: getColor(feature.properties.nb_votes),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

// Events on mouseover:
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    };
    info.update(layer.feature.properties);
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
    });
}

// Reset style when mouseover is finished
function resetHighlight(e) {
    map.layer.resetStyle(e.target);
    info.update();
}

// Info on top right corner:
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// Method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>US Election Results</h4>' +  (props ?
        '<b>' + props.name + '</b><br />' + props.nb_votes + ' votes <br />'+ props.max_voters+' eligible voters.'
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
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);
