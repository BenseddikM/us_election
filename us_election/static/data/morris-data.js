$(function() {

    Morris.Area({
        element: 'morris-area-chart',
        data: [
          {period: '2012-02-24 20:00', Trump: 100,Clinton: 60,Johnson: 5,Stein: 26},
          {period: '2012-02-24 20:10',Trump: 90,Clinton: 30,Johnson: 20,Stein: 10},
          {period: '2012-02-24 20:20',Trump: 20,Clinton: 10,Johnson: 10,Stein: 50},
          {period: '2012-02-24 20:30',Trump: 50,Clinton: 15,Johnson: 40,Stein: 10},
          {period: '2012-02-24 20:40',Trump: 80,Clinton: 80,Johnson: 15,Stein: 60},
          {period: '2012-02-24 20:50',Trump: 20,Clinton: 100,Johnson: 65,Stein: 9},
          {period: '2012-02-24 21:00',Trump: 60,Clinton: 10,Johnson: 15,Stein: 19}
              ],
        xkey: 'period',
        xLabels: "10min",
        ykeys: ['Trump', 'Clinton', 'Johnson','Stein'],
        labels: ['Trump', 'Clinton', 'Johnson','Stein'],
        lineColors:["#DC241f","#00a4e4","#FED105","#17aa5c"],
        resize: true
    });


    Morris.Donut({
        element: 'morris-donut-chart',
        colors:["#DC241f","#00a4e4","#FED105","#17aa5c"],
        data: [
          {label: "Donald Trump – Parti républicain", value: 45.95},
          {label: "Hillary Clinton – Parti démocrate", value: 48.04},
          {label: "Gary Johnson – Parti libertarien", value: 3.29},
          {label: "Jill Stein – Parti vert", value: 1.06}
        ],
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [
          {period: '20:00', Trump: 100,Clinton: 60,Johnson: 5,Stein: 26},
          {period: '20:10',Trump: 90,Clinton: 30,Johnson: 20,Stein: 10},
          {period: '20:20',Trump: 20,Clinton: 10,Johnson: 10,Stein: 50},
          {period: '20:30',Trump: 50,Clinton: 15,Johnson: 40,Stein: 10},
          {period: '20:40',Trump: 80,Clinton: 80,Johnson: 15,Stein: 60},
          {period: '20:50',Trump: 20,Clinton: 100,Johnson: 65,Stein: 9},
          {period: '21:00',Trump: 60,Clinton: 10,Johnson: 15,Stein: 19}
      ],
      xkey: 'period',
      xLabels: "10min",
      ykeys: ['Trump', 'Clinton', 'Johnson','Stein'],
      labels: ['Trump', 'Clinton', 'Johnson','Stein'],
      barColors:["#DC241f","#00a4e4","#FED105","#17aa5c"],
      hideHover: 'auto',
      resize: true
    });

});
