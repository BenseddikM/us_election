// We get data from ajax view and add it to the map and others

function initialAll(data) {
    mapInitial(data);
}

// Launch at beginning
$.getJSON(ajaxurl,
    {minute :10}, // potential parameters
    initialAll);


function refreshAll() {
    // get value of slider
    var minute = $( "#slider-range-min" ).slider( "value" )
    $.getJSON(ajaxurl,
        {
            minute: minute
        }, // potential parameters
        function (data) {
        mapRefresh(data);
    });
}

map.on('dblclick', refreshAll);
