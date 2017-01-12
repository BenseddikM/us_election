// We get data from ajax view and add it to the map and others

function initialAll(data) {
    mapInitialLayers(data["map"]);
}
// Launch at beginning
$.getJSON(ajaxurl,
    {minute :10},
    initialAll);

function updateButtonStatus(){
    var buttonClass="btn btn-success btn-circle btn-lg";
    var faviconClass="fa fa-check";
    $("#mongo-status-circle").attr('class', buttonClass);
    $("#mongo-status-fa").attr('class', faviconClass);
    $('#mongo-refresh').button('reset');
}

function updateTimeUpdateMessage(minute){
    $('#minute_requested').html("    <b>(last update at 8PM + "+minute+" minutes)</b>");
}


function refreshAll(data) {
    mapRefresh(data["map"]);
    updateMainElectorDonut(data["main_electors_donut_data"]);
    updateRegularElectorDonut(data["regular_electors_donut_data"]);
    updateButtonStatus();
    updateTimeUpdateMessage(data["minute_requested"]);
}

function onButtonClick() {
    $('#mongo-refresh').button('loading');
    // get value of slider
    var minute = $( "#slider-range-min" ).slider( "value" )
    $.getJSON(ajaxurl,
        {
            minute: minute
        },
        refreshAll);
}



// Activate button
$('#slider-range-min').on('mouseup', onButtonClick);

//#slider-range-min
//$('#mongo-refresh').on('click', onButtonClick);
