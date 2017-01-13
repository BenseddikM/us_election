function setDonut(elementId) {
    var initialData = [
      {label: "Donald Trump – Parti républicain", value: 0},
      {label: "Hillary Clinton – Parti démocrate", value: 0},
      {label: "Gary Johnson – Parti libertarien", value: 0},
      {label: "Jill Stein – Parti vert", value: 0},
      {label: "Autre", value: 0},
      {label: "No known yet", value: 538}
  ];
    var donut = Morris.Donut({
        element: elementId,
        colors:["#DC241f","blue","#FED105","#17aa5c","#800026", "grey"],
        data: initialData,
        resize: true
    });
    return donut
}
var mainElectorDonut = setDonut('donut-main-electors');


function serverDataToDonutData(data, ignore_unknown=false){
    var goodData = [
    {label: "Autre", value: parseInt(data["Autre"])},
    {label: "Hillary Clinton – Parti démocrate", value: parseInt(data["Clinton"])},
    {label: "Gary Johnson – Parti libertarien", value: parseInt(data["Johnson"])},
    {label: "Jill Stein – Parti vert", value: parseInt(data["Stein"])},
    {label: "Donald Trump – Parti républicain", value: parseInt(data["Trump"])},
    {label: "Not known yet", value: parseInt(data["Unknown"])}
    ];

    // remove undefined items
    var arrayLength = goodData.length;
    var cleanData = []
    for (var i = 0; i < arrayLength; i++) {
        goodData[i]["value"] = goodData[i]["value"] || 0; //j is now 10
    }
    return goodData;
    }


function updateMainElectorDonut(data){
    var goodData = serverDataToDonutData(data);
    //window.alert(JSON.stringify(goodData));
    mainElectorDonut.setData(goodData);
}

var regularElectorDonut = Morris.Donut({
    element: "donut-regular-electors",
    data: [{label: "Unknown", value: 100}],
    colors:["grey","blue","#FED105","#17aa5c","#800026","purple"],
    resize: true
});

function updateRegularElectorDonut(data){
    var goodData = serverDataToDonutData(data, ignore_unknown=true);
    //window.alert(JSON.stringify(goodData));

    regularElectorDonut.setData(goodData);
}
