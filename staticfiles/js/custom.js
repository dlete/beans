// For JQuery UI Calendar
$(function() {
    $( "#id_date" ).datepicker({
        dateFormat: "yy-mm-dd"
    });
});

// select all checkboxes
// for the view transaction_list, so that checking/unchecking the first
// checkbox does check/uncheck all the checkboxes in the page
// http://stackoverflow.com/questions/19164816/jquery-select-all-checkboxes-in-table
// (https://www.sanwebe.com/2014/01/how-to-select-all-deselect-checkboxes-jquery)
$('#select_all_checkboxes').click(function(e){
    var table= $(e.target).closest('table');
    $('td input:checkbox',table).prop('checked',this.checked);
});

//$(function() {
//	$( "#slider-2" ).slider({
//    	value: 60,
//        animate:"slow",
//        orientation: "horizontal"
//   });
//});


// Begin, Slider Bound to Select
$(function() {
    var select = $( "#minbeds" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( select ).slider({
      min: 1,
      max: 6,
      range: "min",
      value: select[ 0 ].selectedIndex + 1,
      slide: function( event, ui ) {
        select[ 0 ].selectedIndex = ui.value - 1;
      }
    });
    $( "#minbeds" ).change(function() {
      slider.slider( "value", this.selectedIndex + 1 );
    });
  });
// End, Slider Bound to Select
