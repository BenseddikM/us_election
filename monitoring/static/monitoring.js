function updateButtonStatus(response){
    var add_info = response['add_info'];
    var printed_info = "Databases available: "+JSON.stringify(add_info['database_names']);
    var status = response['status'];
    var buttonClass;
    var faviconClass;
    if (status==true) {
        buttonClass="btn btn-success btn-circle btn-lg";
        faviconClass="fa fa-check";}
    else if (status==false) {
        buttonClass="btn btn-danger btn-circle btn-lg";
        faviconClass="fa fa-times";}
    else {
        buttonClass="btn";
    }
    $("#mongo-status-circle").attr('class', buttonClass);
    $("#mongo-status-fa").attr('class', faviconClass);
    $("#mongo-add-info").html(printed_info);
}

function createDiv(databaseName){
    var newDiv = "<h3> Database: "+databaseName+"</h3><div id='"+databaseName+"' style='height: 250px;'></div>";
    $("#databases_stats").append(newDiv)
}

function showMongoCollStats(databaseName,databaseData){
Morris.Bar({
  element: databaseName,
  data: databaseData,
  xkey: 'collection',
  ykeys: ['count'],
  labels: ['Count']
});
}

function createDatabasesDivs(response){
    // Now create divs and display bars
    var databasesStats = response['add_info']['databases_stats'];
    var arrayLength = databasesStats.length;
    // clear div if needed
    $("#databases_stats").empty();
    for (var i = 0; i < arrayLength; i++) {
        var databaseName = databasesStats[i]["database"];
        var databaseData = databasesStats[i]["collections"];
        createDiv(databaseName);
        showMongoCollStats(databaseName,databaseData);
    }
}

var btn = $('#mongo-refresh');

function updateHtml(response){
    updateButtonStatus(response);
    createDatabasesDivs(response);
    btn.button('reset');
}

function checkMongoConnection() {
    $.getJSON(mongo_ajax_url,
        {},
        updateHtml);
}


// Activate
btn.on('click', function () {
  $(this).button('loading');
  checkMongoConnection();
});
