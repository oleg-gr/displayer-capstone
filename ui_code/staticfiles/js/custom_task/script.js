$(function(){ //DOM Ready

    // gridster to hold time values
    $("#gridster1 > div").gridster({
            widget_selector : "div",
            widget_margins : [3, 3],
            // each col represents one second, 5 min max for now
            min_cols: 300,
            max_cols: 300,
            // base dimension is 10 seconds
            widget_base_dimensions : [10, 20],
            namespace: '#gridster1'
        }).data('gridster').disable();

    var gridster = $("#gridster2 > div").gridster({
        widget_selector : "div",
        widget_margins : [3, 3],
        // each col represents one second, 5 min max for now
        min_cols: 300,
        max_cols: 300,
        // base dimension is 10 seconds
        widget_base_dimensions : [10, 40],
        // allow resize only in x direction
        resize : {
            enabled : true,
            axes : ['x']
        },
        namespace: '#gridster2'
    }).data('gridster');

});