// For time control

var s =
$( "#slider-range-min" ).slider({
range: "min",
value: 0,
min: 0,
max: 60,
step: 1,
slide: function( event, ui ) {
  $( "#amount" ).val(ui.value +"minutes after 8PM");
}
});
$( "#amount" ).val( $( "#slider-range-min" ).slider( "value" )+" minutes after 8PM" );

function addMinuteSlider() {
  s.slider('value', s.slider('value') + s.slider( "option", "step" ) );
}
