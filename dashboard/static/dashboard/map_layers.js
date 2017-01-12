// Geojson color and style
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

function getColorResult(d) {
    return d == "Trump" ? '#800026' :
           d == "Clinton"  ? 'blue' :
           d == "Unknown"  ? 'grey' :
                      'black';
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


function styleResults(feature) {
    return {
        fillColor: "grey",
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

// Reset style when mouseover is finished
function resetHighlight(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    });
    // map.staticLayer.resetStyle(e.target);
    info.update();
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
    });
}

function mapInitialLayers(data) {
        // Create layers
        map.staticLayer = L.geoJson(
            data,
            {
                style: style,
                onEachFeature: onEachFeature
            }
        );
        map.staticLayer.addTo(map);

        map.resultsLayer = L.geoJson(
            data,
            {
                style: styleResults,
                onEachFeature: onEachFeature
            }
        );
        //map.resultsLayer.addTo(map);


        // Add controls
        var exclusiveLayers = {
            "State weight": map.staticLayer,
            "State results": map.resultsLayer,

        };
        L.control.layers(exclusiveLayers).addTo(map);
    }

function mapRefresh(data) {
    map.staticLayer.clearLayers();
    map.staticLayer.addData(data);
}
