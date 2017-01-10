$(function() {



    Morris.Donut({
        element: 'morris-donut-chart',
        colors:["#DC241f","#00a4e4","#FED105","#17aa5c","grey"],
        data: [
          {label: "Donald Trump – Parti républicain", value: 150},
          {label: "Hillary Clinton – Parti démocrate", value: 130},
          {label: "Gary Johnson – Parti libertarien", value: 15},
          {label: "Jill Stein – Parti vert", value: 10},
          {label: "No known yet", value: 150}
        ],
        resize: true
    });



});
