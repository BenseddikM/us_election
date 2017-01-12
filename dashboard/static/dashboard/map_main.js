
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

// Disable zoom : we use double click to refresh data
map.doubleClickZoom.disable();
map.scrollWheelZoom.disable();
