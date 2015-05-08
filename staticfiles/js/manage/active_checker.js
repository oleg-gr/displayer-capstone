var interval = 15000;

function doActiveCheck() {
    $.getJSON( '/schedules_active_info', function (data) {
                    $("table#schedules_list tbody tr").each( function () {
                        var id = $(this).data("id");
                        var seconds = data[id]['time'];
                        var started = data[id]['active'];
                        var time = convertSecondsToWords(seconds);
                        if (!started) {
                            $(this).removeClass('danger');
                            $(this).removeClass('success');
                            $(this).addClass('info');
                            $(this).find(".active_display").text("The task will start in " + time);
                        } else {
                            if (seconds <= 0) {
                                $(this).removeClass('danger');
                                $(this).removeClass('info');
                                $(this).addClass('success');
                                $(this).find(".active_display").text("The task will run for another " + time);
                            } else {
                                $(this).removeClass('success');
                                $(this).removeClass('info');
                                $(this).addClass('danger');
                                $(this).find(".active_display").text("The task finished " + time + " ago");
                            }
                        }
                    });
                    // Schedule the next
                    setTimeout(doActiveCheck, interval);
                });
}

$(function(){ //DOM Ready

    // Update every interval seconds
    doActiveCheck();

    $(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });

});