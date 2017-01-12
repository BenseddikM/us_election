// We get data from ajax view and add it to the map and others

function initialAll(data) {
    mapInitialLayers(data["map"]);
}
// Launch at beginning
$.getJSON(ajaxurl,
    {minute :0},
    initialAll);

function updateButtonStatus(status){
    if (status == "pending"){
        var buttonClass="btn btn-warning btn-circle btn-lg";
        var faviconClass="fa fa-question";
        $('#button-refresh').button('loading');

    }
    else {
        var buttonClass="btn btn-success btn-circle btn-lg";
        var faviconClass="fa fa-check";
        $('#button-refresh').button('reset');

    }
    $("#status-circle").attr('class', buttonClass);
    $("#status-fa").attr('class', faviconClass);
}

function updateTimeUpdateMessage(minute){
    $('#minute_requested').html("    <b>(last update at 8PM + "+minute+" minutes)</b>");
}


function refreshAll(data) {
    mapRefresh(data["map"]);
    updateMainElectorDonut(data["main_electors_donut_data"]);
    updateRegularElectorDonut(data["regular_electors_donut_data"]);
    updateButtonStatus("ok");
    updateTimeUpdateMessage(data["minute_requested"]);
}

function onButtonClick() {
    //$('#button-refresh').button('loading');
    updateButtonStatus("pending");

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
$('#button-refresh').on('click', onButtonClick);
