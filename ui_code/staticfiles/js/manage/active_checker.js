var interval = 15000;

function doActiveCheck() {
    $.getJSON( '/schedules_active_info', function (data) {
                    $("table#schedules_list tbody tr").each( function () {
                        var id = $(this).data("id");
                        var seconds = data[id];
                        var time = convertSecondsToWords(seconds);
                        if (seconds <= 0) {
                            $(this).removeClass('danger');
                            $(this).addClass('success');
                            $(this).find(".active_display").text("The task will run for another " + time);
                        } else {
                            $(this).removeClass('success');
                            $(this).addClass('danger');
                            $(this).find(".active_display").text("The task finished " + time + " ago");
                        }
                    });
                    // Schedule the next
                    setTimeout(doActiveCheck, interval);
                });
}

function warningMessage(obj, time ) {
    $(obj).find(".active_display").html("Active around " + time + " ago<br>Might indicate a problem");
}

$(function(){ //DOM Ready

    // Update every interval seconds
    doActiveCheck();

    $(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });

});