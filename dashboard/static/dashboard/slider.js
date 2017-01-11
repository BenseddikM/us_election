// For time control
$( function() {
  $( "#slider-range-min" ).slider({
    range: "min",
    value: 10,
    min: 0,
    max: 60,
    slide: function( event, ui ) {
      $( "#amount" ).val(ui.value +"minutes after 8PM");
    }
  });
  $( "#amount" ).val( $( "#slider-range-min" ).slider( "value" )+" minutes after 8PM" );
} );
